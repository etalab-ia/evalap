from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class MetricEnum(str, Enum):
    accuracy = "accuracy"
    f1_score = "f1_score"
    precision = "precision"
    recall = "recall"


class ResultStatus(str, Enum):
    pending = "pending"
    running = "running"
    finished = "finished"


#
# Dataset
#


class DatasetBase(BaseModel):
    name: str
    type_: str


class Dataset(DatasetBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


#
# Model
#


class ModelBase(BaseModel):
    name: str
    prompt_template: str | None = None
    prompt_system: str | None = None
    sampling_params: dict | None = None
    extra_kw: dict | None = None


class Model(ModelBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


#
# Result
#


class ResultBase(BaseModel):
    metric: MetricEnum

    model_config = ConfigDict(from_attributes=True)


class Result(ResultBase):
    id: int
    created_at: datetime
    score: dict
    status: ResultStatus
    generation_table: list[dict] | None = None
    experiment_id: int


#
# Experiment
#


class ExperimentBase(BaseModel):
    name: str
    dataset: Dataset
    metrics: list[MetricEnum]
    model: Model
    dataset_id: int
    model_id: int
    experiment_set_id: int

    model_config = ConfigDict(from_attributes=True, protected_namespaces=())


class ExperimentCreate(ExperimentBase):
    pass


class Experiment(ExperimentBase):
    id: int
    created_at: datetime
    results: list[Result] | None


#
# Experiment Set
#


class ExperimentSetBase(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class ExperimentSetCreate(ExperimentSetBase):
    pass


class ExperimentSet(ExperimentSetBase):
    id: int
    created_at: datetime
    experiments: list[Experiment] | None
