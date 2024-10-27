from dataclasses import dataclass

import api.crud as crud
from api.clients import LlmClient
from api.db import SessionLocal


@dataclass
class MessageAnswer:
    message_type: str  # message router identifier.
    exp_id: str  # the experiment reference
    model_id: str  # the model to generate with.
    line_id: int  # the line number of the dataset.
    query: str  # the name of the observation/metric to process.


async def generate_answer(message: dict):
    """Message is a dict containing the necessary information to process data
    {
        message_type(str): message router identifier.
        exp_id: the experiment reference
        model_id: the model to generate with.
        line_id(int): the line number of the dataset.
        query(str): the name of the observation/metric to process.
    }
    """
    msg = MessageAnswer(**message)
    with SessionLocal() as db:
        print("|", end="", flush=True)
        db_exp = crud.get_experiment(db, msg.exp_id)
        db_model = crud.get_model(db, msg.model_id)

        # Generate answer
        # --
        messages = [{"role": "user", "content": msg.query}]
        if db_model.prompt_system:
            messages = [{"role": "system", "content": db_model.prompt_system}] + messages
        aiclient = LlmClient(base_url=db_model.base_url, api_key=db_model.api_key)
        answer = aiclient.generate(
            model=db_model.name, messages=messages, **db_model.sampling_params
        )

        # Upsert answer
        crud.upsert_answer(db, db_exp.id, msg.line_id, answer=answer)

        # Check if all the answer have been generated.
        if db_exp.num_try == db_exp.dataset.size:
            crud.update_experiment(db, db_exp.id, dict(experiment_status="finished"))


async def generate_observation(message: dict):
    """Message is a dict containing the necessary information to process data
    {
        message_type(str): message router identifie.
        exp_id: the experiment reference
        line_id(int): the line number of the dataset.
        metric_name(str): the name of the observation/metric to process.
        output(str): the actual output of the model.
        output_true(str): the ground truth output.
    }
    """
    with SessionLocal() as db:
        print("+", end="", flush=True)


async def process_task(message: dict):
    """Route and process message"""
    match message["message_type"]:
        case "answer":
            task = generate_answer
        case "observation":
            task = generate_observation
        case _:
            raise NotImplementedError("Message type Unknown")

    return await task(message)
