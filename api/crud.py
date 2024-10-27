from sqlalchemy.orm import Session

import api.models as models
import api.schemas as schemas
from api.metrics import Metric, all_metrics
from api.models import create_object_from_dict

#
# Datasets
#


def get_datasets(db: Session) -> list[models.Dataset]:
    return db.query(models.Dataset).all()


def get_dataset(db: Session, dataset_id: int) -> models.Dataset | None:
    return db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()


def get_model(db: Session, model_id: int) -> models.Model | None:
    return db.query(models.Model).filter(models.Model.id == model_id).first()


#
# Metrics
#


def get_metrics(db: Session) -> list[Metric]:
    return all_metrics.values()


#
# Experiments
#


def create_experiment(db: Session, experiment: schemas.ExperimentCreate) -> models.Experiment:
    db_exp = create_object_from_dict(db, models.Experiment, experiment.to_table_init(db))
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    return db_exp


def remove_experiment(db: Session, experiment_id: int) -> bool:
    experiment = db.query(models.Experiment).get(experiment_id)
    if experiment is None:
        return False
    db.delete(experiment)
    db.commit()
    return True


def get_experiments(db: Session, set_id: int | None = None) -> list[models.Experiment]:
    query = db.query(models.Experiment)
    if set_id:
        query = query.filter(models.Experiment.experiment_set_id == set_id)
    return query.all()


def get_experiment(db: Session, experiment_id: int) -> models.Experiment | None:
    return db.query(models.Experiment).get(experiment_id)


def update_experiment(
    db: Session, experiment_id: int, experiment_update: schemas.ExperimentUpdate | dict
) -> models.Experiment | None:
    if isinstance(experiment_update, dict):
        experiment_update = schemas.ExperimentSetUpdate(**experiment_update)

    experiment = db.query(models.Experiment).get(experiment_id)
    if experiment is None:
        return None
    # Update fields
    for var, value in vars(experiment_update).items():
        setattr(experiment, var, value) if value else None
    db.commit()
    db.refresh(experiment)
    return experiment


#
# Experiment Sets
#


def create_experimentset(
    db: Session, experimentset: schemas.ExperimentSetCreate
) -> models.ExperimentSet:
    db_expset = create_object_from_dict(db, models.ExperimentSet, experimentset.to_table_init(db))
    db.add(db_expset)
    db.commit()
    db.refresh(db_expset)
    return db_expset


def remove_experimentset(db: Session, experimentset_id: int) -> bool:
    experimentset = db.query(models.ExperimentSet).get(experimentset_id)
    if experimentset is None:
        return False
    db.delete(experimentset)
    db.commit()
    return True


def get_experimentsets(db: Session, set_id: int | None = None) -> list[models.ExperimentSet]:
    query = db.query(models.ExperimentSet)
    if set_id:
        query = query.filter(models.ExperimentSet.experimentset_set_id == set_id)
    return query.all()


def get_experimentset(db: Session, experimentset_id: int) -> models.ExperimentSet | None:
    return db.query(models.ExperimentSet).get(experimentset_id)


def update_experimentset(
    db: Session, experimentset_id: int, experimentset_update: schemas.ExperimentSetUpdate | dict
) -> models.ExperimentSet | None:
    if isinstance(experimentset_update, dict):
        experimentset_update = schemas.ExperimentSetUpdate(**experimentset_update)

    experimentset = db.query(models.ExperimentSet).get(experimentset_id)
    if experimentset is None:
        return None
    # Update fields
    for var, value in vars(experimentset_update).items():
        setattr(experimentset, var, value) if value else None
    db.commit()
    db.refresh(experimentset)
    return experimentset


#
# Runner Crud
#


def upsert_answer(db: Session, experiment_id: str, num_line: int, **answer):
    # Check if the record already exists
    db_answer = (
        db.query(models.Answer).filter_by(num_line=num_line, experiment_id=experiment_id).first()
    )

    if db_answer:
        # Update the existing record
        for k, v in answer.items():
            setattr(db_answer, "k", v)
    else:
        # Insert a new record
        db_answer = models.Answer(experiment_id=experiment_id, num_line=num_line, **answer)
        db.add(db_answer)

    db.commit()
    db.refresh(db_answer)
    return db_answer
