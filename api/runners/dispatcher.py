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
    socket.connect("tcp://localhost:5555")

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
        if db_exp.dataset.has_output:
            df = pd.read_json(StringIO(db_exp.dataset.df))
            crud.update_experiment(db, db_exp.id, dict(experiment_status="running_metrics"))
            for result in db_exp.results:
                if result.metric_status != "pending":
                    continue
                result.num_try = 0
                result.num_success = 0
                result.metric_status = "running"
                db.commit()
                for num_line, row in df.iterrows():
                    socket.send_json(
                        {
                            "message_type": MessageType.observation,
                            "exp_id": db_exp.id,
                            "line_id": num_line,
                            "metric_name": result.metric_name,
                            "output": row["output"],
                            "output_true": row.get("output_true"),
                        }
                    )
        elif len(db_exp.answers) > 0:
            df = pd.read_json(StringIO(db_exp.dataset.df))
            crud.update_experiment(db, db_exp.id, dict(experiment_status="running_metrics"))
            for result in db_exp.results:
                if result.metric_status != "pending":
                    continue
                result.num_try = 0
                result.num_success = 0
                result.metric_status = "running"
                db.commit()
                for a in db_exp.answers:
                    row = df.iloc[a.num_line]
                    socket.send_json(
                        {
                            "message_type": MessageType.observation,
                            "exp_id": db_exp.id,
                            "line_id": a.num_line,
                            "metric_name": result.metric_name,
                            "output": a.answer,
                            "output_true": row.get("output_true"),
                        }
                    )

        else:
            raise NotImplementedError(
                "Answer is needed to generate observation for experience: %s" % db_exp.id
            )

    else:
        raise ValueError("Task unkown: %s" % message_type)
