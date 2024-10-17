from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import api.crud as crud
import api.schemas as schemas
from api.db import get_db
from config import Metric

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
    return crud.create_experiment(db, experiment)


@router.delete("/experiment/{id}", status_code=204)
def delete_experiment(id: int, db: Session = Depends(get_db)):
    if not crud.remove_experiment(db, id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return


@router.get("/experiments", response_model=list[schemas.Experiment])
def read_experiments(
    status: str | None = None, set_id: int | None = None, db: Session = Depends(get_db)
):
    return crud.get_experiments(db, status, set_id)


@router.get("/experiment/{id}", response_model=schemas.Experiment)
def read_experiment(id: int, db: Session = Depends(get_db)):
    experiment = crud.get_experiment(db, id)
    if experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return experiment


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
    return crud.create_experimentset(db, experimentset)


@router.delete("/experimentset/{id}", status_code=204)
def delete_experimentset(id: int, db: Session = Depends(get_db)):
    if not crud.remove_experimentset(db, id):
        raise HTTPException(status_code=404, detail="ExperimentSet not found")
    return


@router.get("/experimentsets", response_model=list[schemas.ExperimentSet])
def read_experimentsets(
    status: str | None = None, set_id: int | None = None, db: Session = Depends(get_db)
):
    return crud.get_experimentsets(db, status, set_id)


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
