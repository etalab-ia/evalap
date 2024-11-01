from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import api.crud as crud
import api.schemas as schemas
from api.db import get_db
from api.errors import CustomIntegrityError, SchemaError
from api.metrics import Metric
from api.runners import dispatch_tasks

router = APIRouter()


#
# Datasets
#


@router.get("/datasets", response_model=list[schemas.Dataset])
def read_datasets(db: Session = Depends(get_db)):
    return crud.get_datasets(db)


@router.get("/dataset/{id}", response_model=schemas.Dataset)
def read_dataset(id: int, db: Session = Depends(get_db)):
    dataset = crud.get_dataset(db, id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset


#
# Metrics
#


@router.get("/metrics", response_model=list[Metric])
def read_metrics(db: Session = Depends(get_db)):
    return crud.get_metrics(db)


#
# Experiments
#


@router.post("/experiment", response_model=schemas.Experiment)
def create_experiment(experiment: schemas.ExperimentCreate, db: Session = Depends(get_db)):
    try:
        db_exp = crud.create_experiment(db, experiment)
        if db_exp.dataset.has_answer:
            dispatch_tasks(db, db_exp, "observations")
        else:
            dispatch_tasks(db, db_exp, "answers")

        return db_exp
    except SchemaError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError as e:
        return CustomIntegrityError.from_integrity_error(e.orig).to_http_response()
    except Exception as e:
        raise e


@router.delete("/experiment/{id}", status_code=204)
def delete_experiment(id: int, db: Session = Depends(get_db)):
    if not crud.remove_experiment(db, id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return


@router.get("/experiment/{id}", response_model=schemas.Experiment | schemas.ExperimentWithResults)
def read_experiment(id: int, with_results: bool = False, db: Session = Depends(get_db)):
    experiment = crud.get_experiment(db, id)
    if experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")

    if with_results:
        return schemas.ExperimentWithResults.from_orm(experiment)

    return schemas.Experiment.from_orm(experiment)


@router.patch("/experiment/{id}", response_model=schemas.Experiment)
def update_experiment(
    id: int, experiment_update: schemas.ExperimentCreate, db: Session = Depends(get_db)
):
    experiment = crud.update_experiment(db, id, experiment_update)
    if experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return experiment


#
# Experiment Sets
#


@router.post("/experimentset", response_model=schemas.ExperimentSet)
def create_experimentset(experimentset: schemas.ExperimentSetCreate, db: Session = Depends(get_db)):
    try:
        db_expset = crud.create_experiment(db, experimentset)
        return db_expset
    except SchemaError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError as e:
        return CustomIntegrityError.from_integrity_error(e.orig).to_http_response()
    except Exception as e:
        raise e


@router.delete("/experimentset/{id}", status_code=204)
def delete_experimentset(id: int, db: Session = Depends(get_db)):
    if not crud.remove_experimentset(db, id):
        raise HTTPException(status_code=404, detail="ExperimentSet not found")
    return


@router.get("/experimentset/{id}", response_model=schemas.ExperimentSet)
def read_experimentset(id: int, db: Session = Depends(get_db)):
    experimentset = crud.get_experimentset(db, id)
    if experimentset is None:
        raise HTTPException(status_code=404, detail="ExperimentSet not found")
    return experimentset


@router.patch("/experimentset/{id}", response_model=schemas.ExperimentSet)
def update_experimentset(
    id: int, experimentset_update: schemas.ExperimentSetCreate, db: Session = Depends(get_db)
):
    experimentset = crud.update_experimentset(db, id, experimentset_update)
    if experimentset is None:
        raise HTTPException(status_code=404, detail="ExperimentSet not found")
    return experimentset
