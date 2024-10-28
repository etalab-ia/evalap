from io import StringIO

import pandas as pd
import zmq

import api.crud as crud


def dispatch_tasks(db, db_exp):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://*:5555")

    if not db_exp.dataset.has_answer:
        # Generate answer
        # --
        # iterate the dataset
        df = pd.read_json(StringIO(db_exp.dataset.df))
        for line_num, row in df.iterrows():
            print(line_num)
            socket.send_json(
                {
                    "message_type": "answer",
                    "exp_id": db_exp.id,
                    "model_id": db_exp.model.id,
                    "line_id": line_num,
                    "query": row["query"],
                }
            )

        crud.update_experiment(db, db_exp.id, dict(experiment_status="running_answers"))
        # The runner will check when all answer are finished
        # tu run generation the observation if needed.
    else:
        # Generate observation
        # --
        # iterate metrics and dataset
        metrics = db_exp.metrics
        for metric_name in metrics:
            df = pd.read_json(StringIO(db_exp.dataset.df))
            for line_num, row in df.iterrows():
                socket.send_json(
                    {
                        "message_type": "observation",
                        "exp_id": db_exp.id,
                        "line_id": line_num,
                        "metric_name": metric_name,
                        "output": row["answer"],
                        "output_true": row["answer_true"],
                    }
                )

        crud.update_experiment(db, db_exp.id, dict(experiment_status="running_metrics"))
