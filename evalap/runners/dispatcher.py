import random
import time
from enum import Enum
from io import StringIO

import pandas as pd
import zmq
from sqlalchemy import case, func

import evalap.api.crud as crud
import evalap.api.models as models
import evalap.api.schemas as schemas
from evalap.api.config import ZMQ_SENDER_URL


class MessageType(str, Enum):
    answer = "answers"  # Ask to generate an answer
    observation = "observations"  # Ask to generate an observation


def _fix_answer_num_count(db, db_exp, commit=True):
    # num_try: number of answers.
    # num_success: number of answer where answer is not None.
    counts = (
        db.query(
            func.count(models.Answer.id).label("num_try"),
            func.count(case(((models.Answer.answer != None) & (models.Answer.error_msg == None), 1))).label(
                "num_success"
            ),
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


def _fix_result_num_count(db, result, commit=True):
    # num_try: number of computed result/metric
    # num_success: number of metric where score is not None
    counts = (
        db.query(
            func.count(models.ObservationTable.id).label("num_try"),
            func.count(
                case(
                    (
                        (models.ObservationTable.score != None) & (models.ObservationTable.error_msg == None),
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
        db_exp = _fix_answer_num_count(db, db_exp, commit=False)
        db_exp.num_try = db_exp.num_success
        db.commit()
        for num_line, row in crud.get_dataset_iterator(db_exp):
            # Do not rerun if answer already exist with no error
            r = db.query(models.Answer).filter_by(num_line=num_line, experiment_id=db_exp.id).first()
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
                    "query": row.get("query"),
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

        # Fix and align metric status and count
        blocked_metrics = []
        for result in db_exp.results:
            # wait a random time between 10 and 500 ms to avoid race condition
            time.sleep(random.uniform(50, 500) / 1000)
            db.expire(result, ["metric_status"])
            if result.metric_status == "running":
                blocked_metrics.append(result.id)
            result.metric_status = "running"
            result = _fix_result_num_count(db, result, commit=False)
            result.num_try = result.num_success
            db.commit()

        # Iterate dataset and metrics
        for num_line, row in crud.get_dataset_iterator(db_exp):
            # Retrieve the answer
            a = (
                db.query(models.Answer)
                .filter(models.Answer.experiment_id == db_exp.id, models.Answer.num_line == num_line)
                .first()
            )

            for result in db_exp.results:
                if result.id in blocked_metrics:
                    continue

                # Do not rerun if score already exist with no error
                r = db.query(models.ObservationTable).filter_by(num_line=num_line, result_id=result.id).first()
                if r and r.score is not None and not r.error_msg:
                    continue
                elif r:
                    r.error_msg = None

                sender.send_json(
                    {
                        "message_type": MessageType.observation,
                        "exp_id": db_exp.id,
                        "line_id": num_line,
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
        db_exp = _fix_answer_num_count(db, db_exp, commit=False)
        db_exp.num_try = db_exp.num_success
        db.commit()
        df = pd.read_json(StringIO(db_exp.dataset.df))

        # Failed
        num_line_added = []
        for a in db_exp.answers:
            if a.answer is not None and not a.error_msg:  # @TODO: add a is_failed columns !
                continue

            a.error_msg = None
            row = crud.get_dataset_row(db_exp, a.num_line, df_fallback=df)
            sender.send_json(
                {
                    "message_type": MessageType.answer,
                    "exp_id": db_exp.id,
                    "model_id": db_exp.model.id,
                    "line_id": a.num_line,
                    "query": row.get("query"),
                }
            )
            num_line_added + [a.num_line]

        db.commit()  # for obs.error_msg

        if db_exp.with_vision:
            dataset_size = db_exp.dataset.parquet_size
        else:
            dataset_size = db_exp.dataset.size

        # unfinished
        num_lines = db.query(models.Answer.num_line).filter(models.Answer.experiment_id == expid).all()
        num_lines = [num_line[0] for num_line in num_lines]
        all_lines = db_exp.dataset.sample if db_exp.dataset.sample else range(dataset_size)
        num_lines_missing = [i for i in all_lines if i not in num_line_added and i not in num_lines]
        for num_line in num_lines_missing:
            row = crud.get_dataset_row(db_exp, num_line, df_fallback=df)
            sender.send_json(
                {
                    "message_type": MessageType.answer,
                    "exp_id": db_exp.id,
                    "model_id": db_exp.model.id,
                    "line_id": num_line,
                    "query": row.get("query"),
                }
            )

    # Metrics
    for resultid in set(retry_runs.result_ids + retry_runs.unfinished_result_ids):
        result = crud.get_result(db, resultid)
        db_exp = result.experiment
        db_exp.experiment_status = "running_metrics"
        result.metric_status = "running"
        result = _fix_result_num_count(db, result, commit=False)
        result.num_try = result.num_success
        db.commit()
        df = pd.read_json(StringIO(db_exp.dataset.df))

        # Failed
        num_line_added = []
        for obs in result.observation_table:
            if obs.score is not None and not obs.error_msg:  # @TODO: add a is_failed columns !
                continue

            obs.error_msg = None
            row = crud.get_dataset_row(db_exp, obs.num_line, df_fallback=df)
            answer = crud.get_answer(db, experiment_id=db_exp.id, num_line=obs.num_line)
            if not answer:
                output = row.get("output")
            else:
                output = answer.answer

            sender.send_json(
                {
                    "message_type": MessageType.observation,
                    "exp_id": db_exp.id,
                    "line_id": obs.num_line,
                    "metric_name": result.metric_name,
                    "output": output,
                    "output_true": row.get("output_true"),
                }
            )
            num_line_added + [answer.num_line]

        db.commit()  # for obs.error_msg

        if db_exp.with_vision:
            dataset_size = db_exp.dataset.parquet_size
        else:
            dataset_size = db_exp.dataset.size

        # Unfinished
        num_lines = (
            db.query(models.ObservationTable.num_line)
            .filter(models.ObservationTable.result_id == resultid)
            .all()
        )
        num_lines = [num_line[0] for num_line in num_lines]
        all_lines = db_exp.dataset.sample if db_exp.dataset.sample else range(dataset_size)
        num_lines_missing = [i for i in all_lines if i not in num_line_added and i not in num_lines]
        for num_line in num_lines_missing:
            row = crud.get_dataset_row(db_exp, num_line, df_fallback=df)
            answer = crud.get_answer(db, experiment_id=db_exp.id, num_line=num_line)
            if not answer:
                output = row.get("output")
            else:
                output = answer.answer

            sender.send_json(
                {
                    "message_type": MessageType.observation,
                    "exp_id": db_exp.id,
                    "line_id": num_line,
                    "metric_name": result.metric_name,
                    "output": output,
                    "output_true": row.get("output_true"),
                }
            )

        if all(r.metric_status == "finished" for r in result.experiment.results):
            crud.update_experiment(db, db_exp.id, dict(experiment_status="finished"))

    sender.close()
    context.term()
