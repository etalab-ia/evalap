import random
import time
from enum import Enum
from io import StringIO

import pandas as pd
import zmq
from sqlalchemy import case, func

import eg1.api.crud as crud
import eg1.api.models as models
import eg1.api.schemas as schemas
from eg1.api.config import ZMQ_SENDER_URL
from eg1.logger import logger


class MessageType(str, Enum):
    answer = "answers"  # Ask to generate an answer
    observation = "observations"  # Ask to generate an observation


def fix_answer_num_count(db, db_exp, commit=True):
    # num_try: number of answers.
    # num_success: number of answer where answer is not None.
    counts = (
        db.query(
            func.count(models.Answer.id).label("num_try"),
            func.count(
                case(((models.Answer.answer != None) & (models.Answer.error_msg == None), 1))
            ).label("num_success"),
        )
        .filter(models.Answer.experiment_id == db_exp.id)
        .one()
    )

    db_exp.num_try = counts.num_try
    db_exp.num_success = counts.num_success
    if commit:
        db.commit()
        db.refresh(db_exp)
    return db_exp


def fix_result_num_count(db, result, commit=True):
    # num_try: number of computed result/metric
    # num_success: number of metric where score is not None
    counts = (
        db.query(
            func.count(models.ObservationTable.id).label("num_try"),
            func.count(
                case(
                    (
                        (models.ObservationTable.score != None)
                        & (models.ObservationTable.error_msg == None),
                        1,
                    )
                )
            ).label("num_success"),
        )
        .filter(models.ObservationTable.result_id == result.id)
        .one()
    )

    result.num_try = counts.num_try
    result.num_success = counts.num_success
    if commit:
        db.commit()
        db.refresh(result)
    return result


def dispatch_tasks(db, db_exp, message_type: MessageType):
    context = zmq.Context()
    sender = context.socket(zmq.PUSH)
    sender.connect(ZMQ_SENDER_URL)

    if message_type == MessageType.answer:
        # Generate answer
        # --
        # iterate the dataset
        db_exp.experiment_status = "running_answers"
        db_exp = fix_answer_num_count(db, db_exp, commit=False)
        db_exp.num_try = db_exp.num_success
        db.commit()
        df = pd.read_json(StringIO(db_exp.dataset.df))
        for num_line, row in df.iterrows():
            # Do not rerun if answer already exist with no error
            r = (
                db.query(models.Answer)
                .filter_by(num_line=num_line, experiment_id=db_exp.id)
                .first()
            )
            if r and r.answer and not r.error_msg:
                continue
            elif r:
                r.error_msg = None

            sender.send_json(
                {
                    "message_type": MessageType.answer,
                    "exp_id": db_exp.id,
                    "model_id": db_exp.model.id,
                    "line_id": num_line,
                    "query": row["query"],
                }
            )

        db.commit()
        # The runner will check when all answers are finished
        # and follow with the observations if needed.
    elif message_type == MessageType.observation:
        # Generate observation
        # --
        # iterate metrics and dataset
        if len(db_exp.answers) == 0:
            raise NotImplementedError(
                "No answers available to generate observations for this experiment: %s" % db_exp.id
            )
        db_exp.experiment_status = "running_metrics"
        db.commit()
        df = pd.read_json(StringIO(db_exp.dataset.df))
        for result in db_exp.results:
            # wait a random time between 10 and 500 ms to avoid race condition
            time.sleep(random.uniform(10, 500) / 1000)
            db.expire(result, ["metric_status"])
            if result.metric_status == "running":
                continue
            result.metric_status = "running"
            result = fix_result_num_count(db, result, commit=False)
            result.num_try = result.num_success
            db.commit()
            for a in db_exp.answers:
                # Do not rerun if score already exist with no error
                r = (
                    db.query(models.ObservationTable)
                    .filter_by(num_line=a.num_line, result_id=result.id)
                    .first()
                )
                if r and r.score is not None and not r.error_msg:
                    continue
                elif r:
                    r.error_msg = None

                row = df.iloc[a.num_line]
                sender.send_json(
                    {
                        "message_type": MessageType.observation,
                        "exp_id": db_exp.id,
                        "line_id": a.num_line,
                        "metric_name": result.metric_name,
                        "output": a.answer,
                        "output_true": row.get("output_true"),
                    }
                )

        db.commit()
    else:
        raise ValueError("Task unkown: %s" % message_type)

    sender.close()
    context.term()


def dispatch_retries(db, retry_runs: schemas.RetryRuns):
    context = zmq.Context()
    sender = context.socket(zmq.PUSH)
    sender.connect(ZMQ_SENDER_URL)

    #
    # Retry failed and unfinished expe
    #

    # Answers
    for expid in set(retry_runs.experiment_ids + retry_runs.unfinished_experiment_ids):
        db_exp = crud.get_experiment(db, expid)
        if db_exp is None:
            raise ValueError("should never happen: dprexpnotfound1")

        db_exp.experiment_status = "running_answers"
        db_exp = fix_answer_num_count(db, db_exp, commit=False)
        db_exp.num_try = db_exp.num_success
        db.commit()
        df = pd.read_json(StringIO(db_exp.dataset.df))

        # Failed
        num_line_added = []
        for answer in db_exp.answers:
            if (
                answer.answer is not None and not answer.error_msg
            ):  # @TODO: add a is_failed columns !
                continue

            answer.error_msg = None
            sender.send_json(
                {
                    "message_type": MessageType.answer,
                    "exp_id": db_exp.id,
                    "model_id": db_exp.model.id,
                    "line_id": answer.num_line,
                    "query": df.iloc[answer.num_line]["query"],
                }
            )
            num_line_added + [answer.num_line]

        db.commit()  # for obs.error_msg

        # unfinished
        num_lines = (
            db.query(models.Answer.num_line).filter(models.Answer.experiment_id == expid).all()
        )
        num_lines = [num_line[0] for num_line in num_lines]
        num_lines_missing = [
            i for i in range(db_exp.dataset.size) if i not in num_line_added and i not in num_lines
        ]
        for num_line in num_lines_missing:
            sender.send_json(
                {
                    "message_type": MessageType.answer,
                    "exp_id": db_exp.id,
                    "model_id": db_exp.model.id,
                    "line_id": num_line,
                    "query": df.iloc[num_line]["query"],
                }
            )

    # Metrics
    for resultid in set(retry_runs.result_ids + retry_runs.unfinished_result_ids):
        result = crud.get_result(db, resultid)
        db_exp = result.experiment
        db_exp.experiment_status = "running_metrics"
        result.metric_status = "running"
        result = fix_result_num_count(db, result, commit=False)
        result.num_try = result.num_success
        db.commit()
        df = pd.read_json(StringIO(db_exp.dataset.df))

        # Failed
        num_line_added = []
        for obs in result.observation_table:
            if obs.score is not None and not obs.error_msg:  # @TODO: add a is_failed columns !
                continue

            obs.error_msg = None
            answer = crud.get_answer(db, experiment_id=db_exp.id, num_line=obs.num_line)
            if not answer:
                output = df.iloc[obs.num_line].get("output")
            else:
                output = answer.answer

            sender.send_json(
                {
                    "message_type": MessageType.observation,
                    "exp_id": db_exp.id,
                    "line_id": obs.num_line,
                    "metric_name": result.metric_name,
                    "output": output,
                    "output_true": df.iloc[obs.num_line].get("output_true"),
                }
            )
            num_line_added + [answer.num_line]

        db.commit()  # for obs.error_msg

        # Unfinished
        num_lines = (
            db.query(models.ObservationTable.num_line)
            .filter(models.ObservationTable.result_id == resultid)
            .all()
        )
        num_lines = [num_line[0] for num_line in num_lines]
        num_lines_missing = [
            i for i in range(db_exp.dataset.size) if i not in num_line_added and i not in num_lines
        ]
        for num_line in num_lines_missing:
            answer = crud.get_answer(db, experiment_id=db_exp.id, num_line=num_line)
            if not answer:
                output = df.iloc[num_line].get("output")
            else:
                output = answer.answer

            sender.send_json(
                {
                    "message_type": MessageType.observation,
                    "exp_id": db_exp.id,
                    "line_id": num_line,
                    "metric_name": result.metric_name,
                    "output": output,
                    "output_true": df.iloc[num_line].get("output_true"),
                }
            )

        if all(r.metric_status == "finished" for r in result.experiment.results):
            crud.update_experiment(db, db_exp.id, dict(experiment_status="finished"))

    sender.close()
    context.term()
