from enum import Enum
from io import StringIO

import pandas as pd
import zmq

import api.crud as crud


class MessageType(str, Enum):
    answer = "answers"  # Ask to generate an answer
    observation = "observations"  # Ask to generate an observation


def dispatch_tasks(db, db_exp, message_type: MessageType):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://*:5555")

    if message_type == MessageType.answer:
        # Generate answer
        # --
        # iterate the dataset
        crud.update_experiment(db, db_exp.id, dict(experiment_status="running_answers", num_try=0))
        df = pd.read_json(StringIO(db_exp.dataset.df))
        for num_line, row in df.iterrows():
            socket.send_json(
                {
                    "message_type": MessageType.answer,
                    "exp_id": db_exp.id,
                    "model_id": db_exp.model.id,
                    "line_id": num_line,
                    "query": row["query"],
                }
            )

        # The runner will check when all answer are finished
        # tu run generation the observation if needed.
    elif message_type == MessageType.observation:
        # Generate observation
        # --
        # iterate metrics and dataset
        if db_exp.dataset.has_answer:
            df = pd.read_json(StringIO(db_exp.dataset.df))
            metrics = db_exp.metrics
            crud.update_experiment(db, db_exp.id, dict(experiment_status="running_metrics"))
            for metric_name in metrics:
                for num_line, row in df.iterrows():
                    socket.send_json(
                        {
                            "message_type": MessageType.observation,
                            "exp_id": db_exp.id,
                            "line_id": num_line,
                            "metric_name": metric_name,
                            "output": row["answer"],
                            "output_true": row.get("answer_true"),
                        }
                    )
        elif len(db_exp.answers) > 0:
            metrics = db_exp.metrics
            df = pd.read_json(StringIO(db_exp.dataset.df))
            crud.update_experiment(db, db_exp.id, dict(experiment_status="running_metrics"))
            for metric_name in metrics:
                for a in db_exp.answers:
                    row = df.iloc[a.num_line]
                    socket.send_json(
                        {
                            "message_type": MessageType.observation,
                            "exp_id": db_exp.id,
                            "line_id": a.num_line,
                            "metric_name": metric_name,
                            "output": a.answer,
                            "output_true": row.get("answer_true"),
                        }
                    )

        else:
            raise NotImplementedError(
                "Answer is needed to generate observation for experience: %s" % db_exp.id
            )

    else:
        raise ValueError("Task unkown: %s" % message_type)
