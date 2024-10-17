from sqlalchemy.orm import Session

import api.models as models
import api.schemas as schemas
from config.metrics import Metric, all_metrics

#
# Datasets
#


def get_datasets(db: Session) -> list[models.Dataset]:
    return db.query(models.Dataset).all()


def get_dataset(db: Session, dataset_id: int) -> models.Dataset | None:
    return db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()


#
# Metrics
#


def get_metrics(db: Session) -> list[Metric]:
    return all_metrics.values()


#
# Experiments
#


def create_experiment(db: Session, experiment: schemas.ExperimentCreate) -> models.Experiment:
    db_experiment = models.Experiment(
        name=experiment.name,
        dataset_id=experiment.dataset_id,
        model_id=experiment.model_id,
    )
    db.add(db_experiment)
    # Associate metrics
    for metric in experiment.metrics:
        metric = all_metrics.get(metric)
        if metric:
            db_experiment.metrics.append(metric)
    db.commit()
    db.refresh(db_experiment)
    return db_experiment


def remove_experiment(db: Session, experiment_id: int) -> bool:
    experiment = db.query(models.Experiment).get(experiment_id)
    if experiment is None:
        return False
    db.delete(experiment)
    db.commit()
    return True


def get_experiments(
    db: Session, set_id: int | None = None
) -> list[models.Experiment]:
    query = db.query(models.Experiment)
    if set_id:
        query = query.filter(models.Experiment.experiment_set_id == set_id)
    return query.all()


def get_experiment(db: Session, experiment_id: int) -> models.Experiment | None:
    return db.query(models.Experiment).get(experiment_id)


def update_experiment(
    db: Session, experiment_id: int, experiment_update: schemas.ExperimentCreate
) -> models.Experiment | None:
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


def create_experimentset(db: Session, experimentset: schemas.ExperimentSetCreate) -> models.ExperimentSet:
    db_experimentset = models.ExperimentSet(
        name=experimentset.name,
    )
    db.add(db_experimentset)
    db.commit()
    db.refresh(db_experimentset)
    return db_experimentset


def remove_experimentset(db: Session, experimentset_id: int) -> bool:
    experimentset = db.query(models.ExperimentSet).get(experimentset_id)
    if experimentset is None:
        return False
    db.delete(experimentset)
    db.commit()
    return True


def get_experimentsets(
    db: Session, set_id: int | None = None
) -> list[models.ExperimentSet]:
    query = db.query(models.ExperimentSet)
    if set_id:
        query = query.filter(models.ExperimentSet.experimentset_set_id == set_id)
    return query.all()


def get_experimentset(db: Session, experimentset_id: int) -> models.ExperimentSet | None:
    return db.query(models.ExperimentSet).get(experimentset_id)


def update_experimentset(
    db: Session, experimentset_id: int, experimentset_update: schemas.ExperimentSetCreate
) -> models.ExperimentSet | None:
    experimentset = db.query(models.ExperimentSet).get(experimentset_id)
    if experimentset is None:
        return None
    # Update fields
    for var, value in vars(experimentset_update).items():
        setattr(experimentset, var, value) if value else None
    db.commit()
    db.refresh(experimentset)
    return experimentset
