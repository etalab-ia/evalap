from io import StringIO
from typing import Generator

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import and_, desc, func, select
from sqlalchemy.orm import Session, joinedload, aliased

import evalap.api.models as models
import evalap.api.schemas as schemas
from evalap.api.errors import SchemaError
from evalap.api.metrics import Metric, metric_registry
from evalap.api.models import create_object_from_dict
from evalap.utils import get_parquet_row_by_index

#
# Datasets
#


def create_dataset(db: Session, dataset: schemas.DatasetCreate) -> models.Dataset:
    dataset = dataset.to_table_init(db) if isinstance(dataset, schemas.EgBaseModel) else dataset
    db_dataset = create_object_from_dict(db, models.Dataset, dataset)
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset


def get_datasets(db: Session) -> list[models.Dataset]:
    return db.query(models.Dataset).all()


def get_dataset(db: Session, dataset_id: int) -> models.Dataset | None:
    return db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()


def get_dataset_by_name(db: Session, dataset_name: str) -> models.Dataset | None:
    return db.query(models.Dataset).filter(models.Dataset.name == dataset_name).first()


def get_model(db: Session, model_id: int) -> models.Model | None:
    return db.query(models.Model).filter(models.Model.id == model_id).first()


def update_dataset(
    db: Session, dataset_id: int, dataset_update: schemas.DatasetUpdate | dict
) -> models.Dataset | None:
    if isinstance(dataset_update, dict):
        dataset_update = schemas.DatasetUpdate(**dataset_update)

    db_dataset = db.query(models.Dataset).get(dataset_id)
    if db_dataset is None:
        return None
    # Update fields
    for key, value in vars(dataset_update).items():
        setattr(db_dataset, key, value) if value is not None else None
    db.commit()
    db.refresh(db_dataset)
    return db_dataset


def remove_dataset(db: Session, dataset_id: int) -> bool:
    linked_experiments = (
        db.query(func.count(models.Experiment.id)).filter(models.Experiment.dataset_id == dataset_id).scalar()
    )
    if linked_experiments > 0:
        raise SchemaError(
            f"This dataset is linked to {linked_experiments} experiments.\n"
            "You must either delete linked experiments or associated them to another dataset to remove this one."
        )

    db_dataset = db.query(models.Dataset).get(dataset_id)
    if db_dataset is None:
        return False

    db.delete(db_dataset)
    db.commit()
    # update_db_exp(db, dataset_id, dict(is_archived=True))
    return True


def get_dataset_row(
    db_exp: models.Experiment, line_id: int, df_fallback=None | pd.DataFrame, columns_map=None
) -> dict:
    if db_exp.with_vision:
        row = get_parquet_row_by_index(db_exp.dataset.parquet_path, line_id)
    else:
        if df_fallback is None:
            df = pd.read_json(StringIO(db_exp.dataset.df))
        else:
            df = df_fallback
        row = df.iloc[line_id].to_dict()
        row = {k: (v.item() if isinstance(v, np.generic) else v) for k, v in row.items()}

    for k, v in (db_exp.dataset.columns_map or {}).items():
        row[k] = row[v]

    return row


def get_dataset_iterator(
    db_exp: models.Experiment, columns_map=None
) -> Generator[tuple[int, dict], None, None]:
    if db_exp.with_vision:
        # Parquet based dataset
        pf = pq.ParquetFile(db_exp.dataset.parquet_path)
        batch_size = 10
        batch_number = 0
        for batch in pf.iter_batches(batch_size=batch_size):
            df = batch.to_pandas()
            for num_line, row in df.iterrows():
                row = row.to_dict()
                row = {k: (v.item() if isinstance(v, np.generic) else v) for k, v in row.items()}
                for k, v in (db_exp.dataset.columns_map or {}).items():
                    row[k] = row[v]
                yield num_line + batch_number * batch_size, row

            batch_number += 1
    else:
        # Dataframe based dataset
        df = pd.read_json(StringIO(db_exp.dataset.df))
        for num_line, row in df.iterrows():
            row = row.to_dict()
            row = {k: (v.item() if isinstance(v, np.generic) else v) for k, v in row.items()}
            for k, v in (db_exp.dataset.columns_map or {}).items():
                row[k] = row[v]
            yield num_line, row


#
# Metrics
#


def get_metrics(db: Session) -> list[Metric]:
    return list(metric_registry.get_metrics())


#
# Results
#


def get_answer(
    db: Session,
    answer_id: int | None = None,
    experiment_id: int | None = None,
    num_line: int | None = None,
) -> models.Answer | None:
    if answer_id:
        return db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    elif experiment_id and num_line is not None:
        return db.query(models.Answer).filter_by(experiment_id=experiment_id, num_line=num_line).first()
    else:
        raise ValueError("Should give at list an answer_id or a experiment_id/num_line couple.")


def get_result(
    db: Session,
    result_id: int | None = None,
    experiment_id: int | None = None,
    metric_name: str | None = None,
) -> models.Result | None:
    if result_id:
        return db.query(models.Result).filter(models.Result.id == result_id).first()
    elif experiment_id and metric_name:
        # TODO: unique by name vs configurable metric (always acceded is by result_id)
        return db.query(models.Result).filter_by(experiment_id=experiment_id, metric_name=metric_name).first()
    else:
        raise ValueError("Should give at list an result_id or a couple experiment_id/metric_name couple.")


def create_result(db: Session, result: schemas.ResultCreate) -> models.Result:
    result = result.to_table_init(db) if isinstance(result, schemas.EgBaseModel) else result
    db_result = create_object_from_dict(db, models.Result, result)
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


def update_result(
    db: Session, result_id: int, result_update: schemas.ResultUpdate | dict
) -> models.Result | None:
    if isinstance(result_update, dict):
        result_update = schemas.ResultUpdate(**result_update)

    db_result = db.query(models.Result).get(result_id)
    if db_result is None:
        return None
    # Update fields
    for key, value in vars(result_update).items():
        setattr(db_result, key, value) if value is not None else None
    db.commit()
    db.refresh(db_result)
    return db_result


#
# Experiments
#


def create_experiment(db: Session, experiment: schemas.ExperimentCreate) -> models.Experiment:
    experiment = experiment.to_table_init(db) if isinstance(experiment, schemas.EgBaseModel) else experiment
    db_exp = create_object_from_dict(db, models.Experiment, experiment)
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    return db_exp


def get_experiment(db: Session, experiment_id: int) -> models.Experiment | None:
    return db.query(models.Experiment).get(experiment_id)


def get_experiments(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    backward: bool = False,
    set_id: int | None = None,
    orphan: bool = False,
) -> list[models.Experiment]:
    limit = min(limit, 100)
    query = db.query(models.Experiment).filter_by(is_archived=False)
    if backward:
        query = query.order_by(models.Experiment.id.desc())
    else:
        query = query.order_by(models.Experiment.id.asc())

    if set_id:
        query = query.filter(models.Experiment.experiment_set_id == set_id)
    if orphan:
        query = query.filter(models.Experiment.experiment_set_id == None)
    return query.offset(skip).limit(limit).options(joinedload(models.Experiment.results)).all()


def update_experiment(
    db: Session, experiment_id: int, experiment_update: schemas.ExperimentUpdate | dict
) -> models.Experiment | None:
    if isinstance(experiment_update, dict):
        experiment_update = schemas.ExperimentUpdate(**experiment_update)

    db_exp = db.query(models.Experiment).get(experiment_id)
    if db_exp is None:
        return None
    # Update fields
    for key, value in vars(experiment_update).items():
        setattr(db_exp, key, value) if value is not None else None
        # If experiment_status is set to finished, update all result status too.
        if key == "experiment_status" and value == schemas.ExperimentStatus.finished:
            for result in db_exp.results:
                result.metric_status = schemas.MetricStatus.finished
    db.commit()
    db.refresh(db_exp)
    return db_exp


def remove_experiment(db: Session, experiment_id: int) -> bool:
    db_exp = db.query(models.Experiment).get(experiment_id)
    if db_exp is None:
        return False

    # Delete linked results
    for result in db_exp.results:
        db.delete(result)

    # Delete linked answers
    for answer in db_exp.answers:
        db.delete(answer)

    db.delete(db_exp)
    db.commit()
    # update_db_exp(db, experiment_id, dict(is_archived=True))
    return True


#
# Experiment Sets
#


def create_experimentset(db: Session, experimentset: schemas.ExperimentSetCreate) -> models.ExperimentSet:
    experimentset = (
        experimentset.to_table_init(db) if isinstance(experimentset, schemas.EgBaseModel) else experimentset
    )
    db_expset = create_object_from_dict(db, models.ExperimentSet, experimentset)
    db.add(db_expset)
    db.commit()
    db.refresh(db_expset)
    return db_expset


def get_experimentsets(
    db: Session, skip: int = 0, limit: int = 100, backward: bool = False
) -> list[models.ExperimentSet]:
    query = db.query(models.ExperimentSet)
    if backward:
        query = query.order_by(models.ExperimentSet.id.desc())
    else:
        query = query.order_by(models.ExperimentSet.id.asc())
    return query.offset(skip).limit(limit).all()


def get_experimentset(db: Session, experimentset_id: int) -> models.ExperimentSet | None:
    return db.query(models.ExperimentSet).get(experimentset_id)


def update_experimentset(
    db: Session, experimentset_id: int, experimentset_update: schemas.ExperimentSetUpdate | dict
) -> models.ExperimentSet | None:
    if isinstance(experimentset_update, dict):
        experimentset_update = schemas.ExperimentSetUpdate(**experimentset_update)

    db_expset = db.query(models.ExperimentSet).get(experimentset_id)
    if db_expset is None:
        return None
    # Update fields
    for key, value in vars(experimentset_update).items():
        if key in [
            "experiments"
        ]:  # Solve an sa_instance error  when patching an experiment_set with given experiments...
            continue
        setattr(db_expset, key, value) if value is not None else None
    db.commit()
    db.refresh(db_expset)
    return db_expset


def remove_experimentset(db: Session, experimentset_id: int) -> bool:
    db_expset = db.query(models.ExperimentSet).get(experimentset_id)
    if db_expset is None:
        return False

    for experiment in db_expset.experiments:
        remove_experiment(db, experiment.id)
    db.delete(db_expset)
    db.commit()
    return True


#
# Runner Crud
#


def upsert_answer(db: Session, experiment_id: int, num_line: int, answer: dict) -> models.Answer:
    # Check if the record already exists
    db_answer = db.query(models.Answer).filter_by(num_line=num_line, experiment_id=experiment_id).first()

    if db_answer:
        # Update the existing record
        for k, v in answer.items():
            setattr(db_answer, k, v)
    else:
        # Insert a new record
        db_answer = models.Answer(experiment_id=experiment_id, num_line=num_line, **answer)
        db.add(db_answer)

    db.commit()
    db.refresh(db_answer)
    return db_answer


def upsert_observation(db: Session, result_id: int, num_line: int, observation: dict) -> models.Answer:
    # Check if the record already exists
    db_observation = (
        db.query(models.ObservationTable).filter_by(num_line=num_line, result_id=result_id).first()
    )

    if db_observation:
        # Update the existing record
        for k, v in observation.items():
            setattr(db_observation, k, v)
    else:
        # Insert a new record
        db_observation = models.ObservationTable(result_id=result_id, num_line=num_line, **observation)
        db.add(db_observation)

    db.commit()
    db.refresh(db_observation)
    return db_observation


#
# LeaderBoard
#


def get_leaderboard(
    db: Session,
    metric_name: str = "judge_notator",
    dataset_name: str = None,
    judge_model: str = None,
    limit: int = 100,
    offset: int = 0,
):
    JudgeModel = aliased(models.Model)
    # Subquery
    main_metric_subquery = (
        select(models.Result.experiment_id, func.avg(models.ObservationTable.score).label("main_score"))
        .join(models.ObservationTable, models.Result.id == models.ObservationTable.result_id)
        .where(models.Result.metric_name == metric_name)
        .group_by(models.Result.experiment_id)
        .cte("main_metric")
    )

    query = (
        select(
            models.Experiment.id.label("experiment_id"),
            models.Experiment.name.label("experiment_name"),
            models.Model.name.label("model_name"),
            models.Dataset.name.label("dataset_name"),
            main_metric_subquery.c.main_score.label("main_metric_score"),
            models.Model.system_prompt,
            models.Model.sampling_params,
            models.Model.extra_params,
            models.Experiment.created_at.label("created_at"),
            models.Experiment.experiment_set_id,
            models.ExperimentSet.name.label("experiment_set_name"),
            JudgeModel.name.label("judge_model_name"),
        )
        .join(models.Model, models.Experiment.model_id == models.Model.id)
        .join(JudgeModel, models.Experiment.judge_model_id == JudgeModel.id)
        .join(models.Dataset, models.Experiment.dataset_id == models.Dataset.id)
        .join(main_metric_subquery, models.Experiment.id == main_metric_subquery.c.experiment_id)
        .outerjoin(models.ExperimentSet, models.Experiment.experiment_set_id == models.ExperimentSet.id)
    )

    if dataset_name:
        query = query.where(models.Dataset.name == dataset_name)

    if judge_model:
        query = query.where(JudgeModel.name == judge_model)

    query = query.order_by(desc("main_metric_score")).limit(limit).offset(offset)

    results = db.execute(query).fetchall()

    # Fetch result in leaderboard
    entries = []
    for result in results:
        other_metrics_query = (
            select(models.Result.metric_name, func.avg(models.ObservationTable.score).label("avg_score"))
            .join(models.ObservationTable, models.Result.id == models.ObservationTable.result_id)
            .where(
                and_(
                    models.Result.experiment_id == result.experiment_id,
                    models.Result.metric_name != metric_name,
                )
            )
            .group_by(models.Result.metric_name)
        )
        other_metrics = db.execute(other_metrics_query).fetchall()

        other_metrics_dict = {
            metric: float(score) if score is not None else None for metric, score in other_metrics
        }

        entry = schemas.LeaderboardEntry(
            experiment_id=result.experiment_id,
            experiment_name=result.experiment_name,
            model_name=result.model_name,
            dataset_name=result.dataset_name,
            main_metric_score=float(result.main_metric_score)
            if result.main_metric_score is not None
            else None,
            other_metrics=other_metrics_dict,
            system_prompt=result.system_prompt,
            sampling_param={k: str(v) for k, v in (result.sampling_params or {}).items()},
            extra_param={k: str(v) for k, v in (result.extra_params or {}).items()},
            created_at=result.created_at,
            experiment_set_id=result.experiment_set_id,
            experiment_set_name=result.experiment_set_name,
            judge_model=result.judge_model_name,
        )
        entries.append(entry)

    return schemas.Leaderboard(entries=entries)


#
# Ops
#


def get_ops_metrics(db: Session):
    experiment_sets_count = db.query(func.count(models.ExperimentSet.id)).scalar()
    unique_experiments_count = db.query(func.count(models.Experiment.id)).scalar()
    unique_answers_count = db.query(func.count(models.Answer.id)).scalar()
    unique_metrics_count = db.query(func.count(models.Result.id)).scalar()
    unique_observations_count = db.query(func.count(models.ObservationTable.id)).scalar()

    distinct_models = db.query(models.Model.name, models.Model.aliased_name).distinct().all()
    distinct_models_list = [
        {"name": name, "aliased_name": aliased_name} for name, aliased_name in distinct_models
    ]

    return {
        "experiment_sets": experiment_sets_count,
        "unique_experiments": unique_experiments_count,
        "unique_answers": unique_answers_count,
        "unique_metrics": unique_metrics_count,
        "unique_observations": unique_observations_count,
        "distinct_models": distinct_models_list,
    }


def _convert_range_to_value(value):
    if isinstance(value, dict) and "min" in value and "max" in value:
        return (value["min"] + value["max"]) / 2
    return value


def _extract_emission_values(emission_dict):
    if not emission_dict:
        return {}

    if isinstance(emission_dict, str) and emission_dict.lower() == "null":
        return {}

    if not isinstance(emission_dict, dict):
        return {}

    result = {}
    for key, value in emission_dict.items():
        if isinstance(value, dict):
            if "value" in value:
                result[key] = _convert_range_to_value(value["value"])
            else:
                nested = _extract_emission_values(value)
                result.update({f"{key}_{k}": v for k, v in nested.items()})
    return result


def _aggregate_emissions(entries):
    if not entries:
        return {
            "total_emissions": {},
            "total_entries_with_emissions": 0,
            "first_emission_date": None,
        }

    filtered_entries = [
        e
        for e in entries
        if e.emission_carbon
        and not (isinstance(e.emission_carbon, str) and e.emission_carbon.lower() == "null")
    ]

    if not filtered_entries:
        return {
            "total_emissions": {},
            "total_entries_with_emissions": 0,
            "first_emission_date": None,
        }

    first_emission_date = min(e.created_at for e in filtered_entries)
    total_emissions = {
        k: 0
        for k in [
            "energy",
            "gwp",
            "adpe",
            "pe",
            "usage_energy",
            "usage_gwp",
            "usage_adpe",
            "usage_pe",
            "embodied_gwp",
            "embodied_adpe",
            "embodied_pe",
        ]
    }

    for entry in filtered_entries:
        emission_carbon = entry.emission_carbon
        if isinstance(emission_carbon, str) and emission_carbon.lower() == "null":
            emissions = {}
        elif isinstance(emission_carbon, dict):
            emissions = _extract_emission_values(emission_carbon)
        else:
            emissions = {}

        for key in total_emissions:
            total_emissions[key] += emissions.get(key, 0)

    return {
        "total_emissions": total_emissions,
        "total_entries_with_emissions": len(filtered_entries),
        "first_emission_date": first_emission_date,
    }


def get_ops_eco_answers(db: Session):
    answers = db.query(models.Answer).filter(models.Answer.emission_carbon.isnot(None)).all()
    result = _aggregate_emissions(answers)
    return result


def get_ops_eco_observation_table(db: Session):
    observations = (
        db.query(models.ObservationTable).filter(models.ObservationTable.emission_carbon.isnot(None)).all()
    )
    result = _aggregate_emissions(observations)
    return result


#
# LOCUST
#


def create_locustrun(db: Session, run: schemas.LocustRunCreate) -> models.LocustRun:
    run = run.to_table_init(db) if isinstance(run, schemas.EgBaseModel) else run
    db_run = create_object_from_dict(db, models.LocustRun, run)
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run


def get_locustrun(db: Session, run_id: int) -> models.LocustRun | None:
    return db.query(models.LocustRun).filter(models.LocustRun.id == run_id).first()


def get_locustruns(
    db: Session, skip: int = 0, limit: int = 100, backward: bool = False
) -> list[models.LocustRun]:
    query = db.query(models.LocustRun)
    if backward:
        query = query.order_by(models.LocustRun.id.desc())
    else:
        query = query.order_by(models.LocustRun.id.asc())
    return query.offset(skip).limit(limit).all()


#
# LOAD TESTING
#


def create_loadtesting(db: Session, run: schemas.LoadTestingCreate) -> models.LoadTesting:
    run = run.to_table_init(db) if isinstance(run, schemas.EgBaseModel) else run
    db_run = create_object_from_dict(db, models.LoadTesting, run)
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run


def get_loadtesting(db: Session, run_id: int) -> models.LoadTesting | None:
    return db.query(models.LoadTesting).filter(models.LoadTesting.id == run_id).first()


def remove_loadtesting(db: Session, run_id: int) -> bool:
    load_testing = db.query(models.LoadTesting).filter(models.LoadTesting.id == run_id).first()
    if not load_testing:
        return False

    db.delete(load_testing)
    db.commit()
    return True


def get_loadtestings(
    db: Session, skip: int = 0, limit: int = 100, backward: bool = False
) -> list[models.LoadTesting]:
    query = db.query(models.LoadTesting)
    if backward:
        query = query.order_by(models.LoadTesting.id.desc())
    else:
        query = query.order_by(models.LoadTesting.id.asc())
    return query.offset(skip).limit(limit).all()
