import logging
import traceback
from dataclasses import dataclass
from io import StringIO

import pandas as pd
from sqlalchemy import update

import api.crud as crud
import api.models as models
from api.clients import LlmClient
from api.db import SessionLocal
from api.metrics import metric_registry
from api.runners import MessageType, dispatch_tasks


@dataclass
class MessageAnswer:
    message_type: MessageType  # message router identifier
    exp_id: str  # the experiment reference
    model_id: str  # the model to generate with
    line_id: int  # the line number of the dataset
    query: str  # the name of the observation/metric to process


def generate_answer(message: dict):
    """Message is a MessageAnswer dict containing the necessary information to process data"""
    msg = MessageAnswer(**message)
    with SessionLocal() as db:
        print("+", end="", flush=True)
        exp = crud.get_experiment(db, msg.exp_id)
        model = crud.get_model(db, msg.model_id)
        sampling_params = model.sampling_params or {}
        answer = None
        error_msg = None
        try:
            # Generate answer
            # --
            messages = [{"role": "user", "content": msg.query}]
            if model.prompt_system:
                messages = [{"role": "system", "content": model.prompt_system}] + messages
            aiclient = LlmClient(base_url=model.base_url, api_key=model.api_key)
            result = aiclient.generate(model=model.name, messages=messages, **sampling_params)
            answer = result.choices[0].message.content

            # Upsert answer
            crud.upsert_answer(db, exp.id, msg.line_id, dict(answer=answer))

        except Exception as e:
            error_msg = "Generation failed with error: %s" % e
            logging.debug(traceback.print_exc())
            logging.error(error_msg)

        finally:
            # Ensure atomic transaction
            stmt = (
                update(models.Experiment)
                .where(models.Experiment.id == exp.id)
                .values(
                    num_try=models.Experiment.num_try + 1,
                    num_success=models.Experiment.num_success + (1 if answer else 0),
                )
                .returning(models.Experiment)
            )
            exp = db.execute(stmt).scalars().one()
            db.commit()

            if error_msg:
                crud.upsert_answer(db, exp.id, msg.line_id, dict(error_msg=error_msg))

        # Check if all the answer have been generated.
        if exp.num_try >= exp.dataset.size:
            dispatch_tasks(db, exp, MessageType.observation)


@dataclass
class MessageObservation:
    message_type: MessageType  # message router identifier
    exp_id: str  # the experiment reference
    line_id: int  # the line number of the dataset
    metric_name: str  # the name of the observation/metric to process
    output: str  # The actual output of the model
    output_true: str | None = None  # The ground truth output


def generate_observation(message: dict):
    """Message is a MessageObservation dict containing the necessary information to process data"""
    msg = MessageObservation(**message)
    with SessionLocal() as db:
        print(".", end="", flush=True)
        result = crud.get_result(db, experiment_id=msg.exp_id, metric_name=msg.metric_name)
        score = None
        observation = None
        error_msg = None
        try:
            # Generate observation/metric
            # --
            # Get the metric from registry
            metric  = metric_registry.get_metric(msg.metric_name)
            metric_fun = metric_registry.get_metric_function(msg.metric_name)
            metric_params = {}
            requires = [r for r in metric.require if r not in ["output", "output_true"]]
            if not metric_fun:
                raise ValueError(f"Metric {msg.metric_name} not found for experiment {msg.exp_id}")
            for require in requires:
                # Add extra inputs required by the metric
                dataset = result.experiment.dataset
                df = pd.read_json(StringIO(dataset.df))
                metric_params[require] = df.iloc[msg.line_id][require]
            # Compute metric
            metric_result = metric_fun(msg.output, msg.output_true, **metric_params)
            if isinstance(metric_result, tuple):
                score, observation = metric_result
            else:
                score = metric_result

            # Upsert obsevation
            crud.upsert_observation(
                db, result.id, msg.line_id, dict(observation=observation, score=score)
            )

        except Exception as e:
            error_msg = f"Observation {msg.metric_name} failed with error: %s" % e
            logging.debug(traceback.print_exc())
            logging.error(error_msg)
        finally:
            # Ensure atomic transaction
            stmt = (
                update(models.Result)
                .where(models.Result.id == result.id)
                .values(
                    num_try=models.Result.num_try + 1,
                    num_success=models.Result.num_success + (1 if score is not None else 0),
                )
                .returning(models.Result)
            )
            result = db.execute(stmt).scalars().one()
            db.commit()

            if error_msg:
                crud.upsert_observation(db, result.id, msg.line_id, dict(error_msg=error_msg))

        # Check if all the answer have been generated.
        if result.num_try >= result.experiment.dataset.size:
            # @DEBUG: partially finished - check all metrics...
            crud.update_experiment(db, msg.exp_id, dict(experiment_status="finished"))


def process_task(message: dict):
    """Route and process message"""
    match message["message_type"]:
        case MessageType.answer:
            task = generate_answer
        case MessageType.observation:
            task = generate_observation
        case _:
            raise NotImplementedError("Message type Unknown")

    return task(message)
