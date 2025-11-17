import logging
import traceback
from dataclasses import dataclass, field

from sqlalchemy import update

import evalap.api.crud as crud
import evalap.api.models as models
from evalap.api.config import DEFAULT_JUDGE_MODEL
from evalap.api.db import SessionLocal, get_db_context
from evalap.api.metrics import get_judge_model, metric_registry
from evalap.clients import MCPBridgeClient, multi_step_generate, split_think_answer
from evalap.logger import logger
from evalap.runners import MessageType, dispatch_tasks
from evalap.utils import Timer, get_parquet_row_by_index, image_to_base64
from evalap.utils_eco import impact_carbon


@dataclass
class MessageAnswer:
    message_type: MessageType  # message router identifier
    exp_id: str  # the experiment reference
    model_id: str  # the model to generate with
    line_id: int  # the line number of the dataset
    query: str  # the name of the observation/metric to process
    follow_observation: bool = field(
        default=True
    )  # launch the observation dispacher once anwsers have been generated.


def generate_answer(message: dict, mcp_bridge: MCPBridgeClient | None):
    """Message is a MessageAnswer dict containing the necessary information to process data"""
    msg = MessageAnswer(**message)
    print("+", end="", flush=True)

    # Phase A: load DB metadata in a short-lived transaction
    with get_db_context() as db:
        exp = crud.get_experiment(db, msg.exp_id)
        model = crud.get_model(db, msg.model_id)
        if exp is None or model is None:
            logger.error("Experiment %s or model %s not found", msg.exp_id, msg.model_id)
            return

        exp_meta = {
            "id": exp.id,
            "with_vision": exp.with_vision,
            "dataset_size": crud.get_effective_dataset_size(exp),
            "parquet_path": exp.dataset.parquet_path if exp.with_vision else None,
        }

        model_meta = {
            "name": model.name,
            "base_url": model.base_url,
            "api_key": model.api_key,
            "system_prompt": model.system_prompt,
            "prelude_prompt": model.prelude_prompt,
            "sampling_params": model.sampling_params or {},
            "extra_params": model.extra_params or {},
        }

    dataset_size = exp_meta["dataset_size"]
    with_vision = exp_meta["with_vision"]
    parquet_path = exp_meta["parquet_path"]
    model_name = model_meta["name"]
    model_base_url = model_meta["base_url"]
    model_api_key = model_meta["api_key"]
    system_prompt = model_meta["system_prompt"]
    prelude_prompt = model_meta["prelude_prompt"]
    sampling_params = model_meta["sampling_params"]
    extra_params = model_meta["extra_params"]
    sampling_params_plus = sampling_params | extra_params

    # Phase B: LLM generation and processing (no DB session)
    _tools = sampling_params_plus.pop("_tools_", None)
    if _tools and mcp_bridge:
        tools = mcp_bridge.tools2openai(_tools)
        sampling_params_plus["tools"] = tools

    query = msg.query or ""
    query = "\n\n".join([prelude_prompt, query]) if prelude_prompt else query
    answer = None
    error_msg = None

    try:
        if with_vision:
            if msg.line_id >= 100:
                # @DEBUG/@PERF
                raise ValueError("limit to 100 input for vision")

            pf_row = get_parquet_row_by_index(parquet_path, msg.line_id)
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": query},
                        {
                            "type": "image_url",
                            "image_url": {"url": "data:image/png;base64," + image_to_base64(pf_row["img"])},
                        },
                    ],
                }
            ]
        else:
            messages = [{"role": "user", "content": query}]

        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages

        with Timer() as timer:
            result, steps = multi_step_generate(
                model_base_url=model_base_url,
                model_api_key=model_api_key,
                model_name=model_name,
                messages=messages,
                sampling_params=sampling_params_plus,
                mcp_bridge=mcp_bridge,
            )

        answer = result.choices[0].message.content
        think = None
        steps = steps or None
        context = None
        retrieval_context = None

        # Extract Retrieval Context
        # --
        # RAG and context decoding from tools steps result
        if steps:
            context = [x["tool_result"] for step in steps for x in step]
            retrieval_context = [x for c in context for x in c.split("\n---\n")]
            if len(context) == len(retrieval_context):
                # @improve: better differentiate context from retrieval_contexdt from tool calls
                retrieval_context = None
        # RAG and context from chat response
        if result.search_results:
            retrieval_context = [c.chunk.content for c in result.search_results]

        # Thinking token extraction
        if answer:
            think, answer = split_think_answer(answer)

        # Carbon emission
        try:
            emission_carbon = impact_carbon(
                model_name, model_base_url, result.usage.completion_tokens, timer.execution_time
            )

        except Exception as e:  # noqa: PERF203
            logger.error("Error during calcul carbon impact : %s", e)
            emission_carbon = None

    except Exception as e:  # noqa: PERF203
        error_msg = "Generation failed with error: %s" % e
        logging.debug(traceback.print_exc())
        logging.error(error_msg)
        emission_carbon = None
        think = None
        context = None
        retrieval_context = None
        result = None

    # Phase C: persist answer and update experiment counters
    with get_db_context() as db:
        if result is not None:
            crud.upsert_answer(
                db,
                msg.exp_id,
                msg.line_id,
                dict(
                    answer=answer,
                    think=think,
                    execution_time=timer.execution_time,
                    nb_tokens_prompt=result.usage.prompt_tokens,
                    nb_tokens_completion=result.usage.completion_tokens,
                    context=context,
                    retrieval_context=retrieval_context,
                    nb_tool_calls=sum(len(s) for s in steps) if steps else 0,
                    tool_steps=steps,
                    emission_carbon=emission_carbon,
                ),
            )

        stmt = (
            update(models.Experiment)
            .where(models.Experiment.id == msg.exp_id)
            .values(
                num_try=models.Experiment.num_try + 1,
                num_success=models.Experiment.num_success + (1 if answer else 0),
            )
            .returning(models.Experiment)
        )
        db_exp = db.execute(stmt).scalars().one()

        if error_msg:
            crud.upsert_answer(db, msg.exp_id, msg.line_id, dict(error_msg=error_msg))

        current_num_try = db_exp.num_try

    # Phase D: maybe trigger observations in a separate short-lived transaction
    if current_num_try >= dataset_size and msg.follow_observation:
        with get_db_context() as db:
            db_exp = crud.get_experiment(db, msg.exp_id)
            if db_exp is not None:
                dispatch_tasks(db, db_exp, MessageType.observation)


@dataclass
class MessageObservation:
    message_type: MessageType  # message router identifier
    exp_id: str  # the experiment reference
    line_id: int  # the line number of the dataset
    metric_name: str  # the name of the observation/metric to process
    output: str  # The actual output of the model
    output_true: str | None = None  # The ground truth output


def generate_observation(message: dict, mcp_bridge: MCPBridgeClient):
    """Message is a MessageObservation dict containing the necessary information to process data"""
    msg = MessageObservation(**message)
    print(".", end="", flush=True)

    # Phase A: load metadata in short-lived transaction
    with get_db_context() as db:
        result_obj = crud.get_result(db, experiment_id=msg.exp_id, metric_name=msg.metric_name)
        if result_obj is None:
            logger.error("Result not found for experiment %s, metric %s", msg.exp_id, msg.metric_name)
            return

        experiment = result_obj.experiment
        judge_model_schema = get_judge_model(experiment.judge_model or DEFAULT_JUDGE_MODEL)

        result_meta = {
            "id": result_obj.id,
            "experiment_id": experiment.id,
            "metric_params": result_obj.metric_params or {},
            "dataset_size": crud.get_effective_dataset_size(experiment),
            "judge_model": judge_model_schema,
        }

        answer_obj = crud.get_answer(db, experiment_id=msg.exp_id, num_line=msg.line_id)
        dataset_row = crud.get_dataset_row(experiment, msg.line_id)

        answer_meta = None
        if answer_obj:
            answer_meta = {
                "execution_time": answer_obj.execution_time,
                "nb_tokens_prompt": answer_obj.nb_tokens_prompt,
                "nb_tokens_completion": answer_obj.nb_tokens_completion,
                "nb_tool_calls": answer_obj.nb_tool_calls,
                "retrieval_context": answer_obj.retrieval_context,
                "context": answer_obj.context,
                "emission_carbon": answer_obj.emission_carbon,
            }

    metadata = {}
    if answer_meta:
        metadata.update(
            {
                "generation_time": answer_meta["execution_time"],
                "nb_tokens_prompt": answer_meta["nb_tokens_prompt"],
                "nb_tokens_completion": answer_meta["nb_tokens_completion"],
                "nb_tool_calls": answer_meta["nb_tool_calls"],
                "retrieval_context": answer_meta["retrieval_context"],
                "context": answer_meta["context"],
                "emission_carbon": answer_meta["emission_carbon"],
            }
        )

    score = None
    observation = None
    obs_result = None
    error_msg = None
    emission_carbon = None
    ignore_error = False
    observation_payload = None

    metric = metric_registry.get_metric(msg.metric_name)
    metric_fun = metric_registry.get_metric_function(msg.metric_name)
    if not metric_fun:
        logger.error("Metric '%s' not found for experiment '%s'", msg.metric_name, msg.exp_id)
        return

    metric_params = {"metadata": metadata}
    require_extra = []
    if result_meta["metric_params"]:
        metric_params.update(result_meta["metric_params"])
        prompt = result_meta["metric_params"].get("prompt")
        if prompt:
            require_extra = metric_registry.get_require_from_prompt_template(prompt)

    judge_model = result_meta["judge_model"]
    metric_params["model"] = judge_model

    try:
        for require in metric.require + require_extra:
            if require in ["output", "output_true"]:
                if not getattr(msg, require):
                    raise ValueError(f"The metric '{msg.metric_name}' require a non null `{require}` value.")
                continue

            # Don't override existing metric_params
            if require not in metric_params or metric_params.get(require) is None:
                try:
                    metric_params[require] = dataset_row[require]
                except KeyError:
                    metric_params[require] = metadata.get(require)

            if metric_params.get(require) is None:
                if require in ["context", "retrieval_context"]:
                    ignore_error = True
                raise ValueError(f"The metric '{msg.metric_name}' require a non null `{require}` value.")

        with Timer() as timer:
            metric_result = metric_fun(msg.output, msg.output_true, **metric_params)

        if isinstance(metric_result, tuple):
            score, observation, obs_result = metric_result
        else:
            score = metric_result

        if score is not None and hasattr(score, "item"):
            score = score.item()
        if score is not None and not isinstance(score, (float, int)):
            raise ValueError("Unsupported score type: %s %s" % (type(score), score))

        if obs_result and hasattr(obs_result, "usage") and hasattr(obs_result.usage, "completion_tokens"):
            try:
                emission_carbon = impact_carbon(
                    judge_model.name,
                    judge_model.base_url,
                    obs_result.usage.completion_tokens,
                    timer.execution_time,
                )
            except Exception as exc:  # noqa: PERF203
                logger.info("Error during calcul carbon impact : %s", exc)
                emission_carbon = None

        observation_payload = {
            "observation": observation,
            "score": score,
            "execution_time": int(timer.execution_time),
            "emission_carbon": emission_carbon,
        }

    except Exception as exc:  # noqa: PERF203
        if ignore_error:
            error_msg = f"Ignoring '{msg.metric_name}' with missing require field."
            logging.warning(error_msg)
        else:
            error_msg = f"Observation '{msg.metric_name}' failed with error: {exc}"
            logging.debug(traceback.print_exc())
            logging.error(error_msg)

    with get_db_context() as db:
        if observation_payload and score is not None:
            crud.upsert_observation(db, result_meta["id"], msg.line_id, observation_payload)

        stmt = (
            update(models.Result)
            .where(models.Result.id == result_meta["id"])
            .values(
                num_try=models.Result.num_try + 1,
                num_success=models.Result.num_success + (1 if (score is not None or ignore_error) else 0),
            )
            .returning(models.Result)
        )
        updated_result = db.execute(stmt).scalars().one()

        if error_msg:
            crud.upsert_observation(db, result_meta["id"], msg.line_id, dict(error_msg=error_msg))

        current_num_try = updated_result.num_try

    dataset_size = result_meta["dataset_size"]

    if current_num_try >= dataset_size:
        with get_db_context() as db:
            crud.update_result(db, result_meta["id"], dict(metric_status="finished"))
            print("x", end="", flush=True)
            exp = crud.get_experiment(db, result_meta["experiment_id"])
            if exp and all(r.metric_status == "finished" for r in exp.results):
                crud.update_experiment(db, msg.exp_id, dict(experiment_status="finished"))
                print("$", end="", flush=True)


def process_task(message: dict, mcp_bridge: MCPBridgeClient | None):
    """Route and process message"""
    match message["message_type"]:
        case MessageType.answer:
            task = generate_answer
        case MessageType.observation:
            task = generate_observation
        case _:
            raise NotImplementedError("Message type Unknown")

    return task(message, mcp_bridge)
