import logging
from dataclasses import dataclass

from sqlalchemy import select

import api.crud as crud
import api.models as models
from api.clients import LlmClient
from api.db import SessionLocal


@dataclass
class MessageAnswer:
    message_type: str  # message router identifier.
    exp_id: str  # the experiment reference
    model_id: str  # the model to generate with.
    line_id: int  # the line number of the dataset.
    query: str  # the name of the observation/metric to process.


def generate_answer(message: dict):
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
        print("+", end="", flush=True)
        exp = crud.get_model(db, msg.model_id)
        model = crud.get_model(db, msg.model_id)
        sampling_params = model.sampling_params or {}

        answer = None
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
            crud.upsert_answer(db, exp.id, msg.line_id, answer=answer)

        except Exception as e:
            logging.warning("Generation error: %s" % e)
        finally:
            # Ensure atomic transaction
            # @TODO: crud.get_experiment(db, expid, lock=True)
            db_exp = db.execute(
                select(models.Experiment)
                .where(models.Experiment.id == msg.exp_id)
                .with_for_update()
            ).scalar_one()

            db_exp.num_try += 1
            db_exp.num_success += 1 if answer else 0

            db.commit()

        # Check if all the answer have been generated.
        if db_exp.num_try == db_exp.dataset.size:
            crud.update_experiment(db, db_exp.id, dict(experiment_status="finished"))


def generate_observation(message: dict):
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
        print(".", end="", flush=True)


def process_task(message: dict):
    """Route and process message"""
    match message["message_type"]:
        case "answer":
            task = generate_answer
        case "observation":
            task = generate_observation
        case _:
            raise NotImplementedError("Message type Unknown")

    return task(message)
