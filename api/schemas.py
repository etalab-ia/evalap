from datetime import datetime
from enum import Enum
from io import StringIO
from typing import Optional

import pandas as pd
from pydantic import BaseModel, ConfigDict, create_model
from sqlalchemy.orm import Session

import api.models as models
from api.errors import SchemaError
from api.metrics import metric_registry


#
# Custom BaseModel
#
class EgBaseModel(BaseModel):
    def recurse_table_init(self, db: Session) -> dict:
        obj = self.model_dump()
        for k, v in obj.items():
            sub_schema = getattr(self, k)
            if hasattr(sub_schema, "to_table_init"):
                obj[k] = sub_schema.to_table_init(db)
            elif isinstance(sub_schema, list):
                obj[k] = [
                    o.recurse_table_init(db) if isinstance(o, BaseModel) else o for o in sub_schema
                ]

        return obj

    def to_table_init(self, db: Session):
        return self.model_dump()


#
# Enum
#

MetricEnum = Enum(
    "MetricEnum", {name: name for name in metric_registry.get_metric_names()}, type=str
)


class ExperimentStatus(str, Enum):
    pending = "pending"
    running_answers = "running_answers"
    running_metrics = "running_metrics"
    finished = "finished"


#
# Dataset
#


class DatasetBase(EgBaseModel):
    name: str
    df: str  # from_json

    model_config = ConfigDict(from_attributes=True)


class DatasetCreate(DatasetBase):
    def to_table_init(self, db: Session) -> dict:
        obj = self.recurse_table_init(db)

        # Handle dataframe
        try:
            df = pd.read_json(StringIO(self.df))
        except ValueError:
            raise SchemaError("'df' should be a readable dataframe. Use df.to_json()...")

        has_query = "query" in df.columns
        has_answer = "answer" in df.columns
        has_answer_true = "answer_true" in df.columns

        if not (has_query or has_answer):
            raise SchemaError("Your dataset needs at least a column 'query' or 'answer'.")

        return {
            "has_query": has_query,
            "has_answer": has_answer,
            "has_answer_true": has_answer_true,
            "size": len(df),
            **obj,
        }


class Dataset(DatasetBase):
    id: int
    has_query: bool
    has_answer: bool
    has_answer_true: bool
    size: int


#
# Model
#


class ModelBase(EgBaseModel):
    name: str
    base_url: str
    api_key: str
    prompt_system: str | None = None
    sampling_params: dict | None = None
    extra_kw: dict | None = None

    model_config = ConfigDict(from_attributes=True)


class ModelCreate(ModelBase):
    pass


class Model(ModelBase):
    id: int


#
# Result
#


class Answer(EgBaseModel):
    id: int
    created_at: datetime
    answer: str | None
    num_line: int
    error_msg: str | None

    model_config = ConfigDict(from_attributes=True)


class Observation(EgBaseModel):
    id: int
    created_at: datetime
    score: float | None
    observation: str | None  # json
    num_line: int
    error_msg: str | None

    model_config = ConfigDict(from_attributes=True)


class ResultBase(EgBaseModel):
    metric_name: MetricEnum

    model_config = ConfigDict(from_attributes=True)


class Result(ResultBase):
    id: int
    created_at: datetime
    observation_table: list[Observation]
    num_try: int
    num_success: int
    experiment_id: int


#
# Experiment
#


class ExperimentBase(EgBaseModel):
    name: str
    metrics: list[MetricEnum]
    readme: str | None = None
    experiment_set_id: int | None = None

    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

    skip_answers_generation: bool = False


class ExperimentCreate(ExperimentBase):
    dataset: DatasetCreate | str
    model: ModelCreate | None = None

    def to_table_init(self, db: Session) -> dict:
        obj = self.recurse_table_init(db)

        # Handle Dataset
        if isinstance(self.dataset, str):
            dataset = db.query(models.Dataset).filter_by(name=self.dataset).first()
            if not dataset:
                raise SchemaError("Dataset not found")
        else:
            dataset = models.Dataset(**obj["dataset"])
        obj["dataset"] = dataset

        # Handle Results
        results = []
        for metric_name in self.metrics:
            results.append({"metric_name": metric_name})
        obj["results"] = results

        # Validate Model and metric compatibility
        mr = metric_registry
        needs_answer = any("output" in mr.get_metric(m).require for m in self.metrics)
        needs_answer_true = any("output_true" in mr.get_metric(m).require for m in self.metrics)
        if needs_answer and not self.model and not dataset.has_answer:
            raise SchemaError(
                "You need to provide an answer for this metric. "
                "Either set a model to generate it or provide a dataset with the 'answer' field."
            )
        if needs_answer and not dataset.has_answer and not dataset.has_query:
            raise SchemaError(
                "You need to provide an answer for this metric. "
                "Either provide a dataset with the 'query' field to generate the answer or with an 'answer' field if have generated it yourself."
            )

        if needs_answer_true and not dataset.has_answer_true:
            raise SchemaError(
                "You need to provide a ground truth for this metric. "
                "Your dataset needs to have an 'answer_true' field."
            )

        return {
            "experiment_status": "pending",
            **obj,
        }


class Experiment(ExperimentBase):
    id: int
    created_at: datetime
    experiment_status: ExperimentStatus
    num_try: int
    num_success: int

    dataset_id: int
    model_id: int


class ExperimentWithResults(Experiment):
    results: list[Result] | None


class ExperimentWithAnswers(Experiment):
    answers: list[Answer] | None


class ExperimentFull(Experiment):
    answers: list[Answer] | None
    results: list[Result] | None


ExperimentUpdate = create_model(
    "Experiment",
    **{
        field_name: (Optional[field], None)
        for field_name, field in Experiment.__annotations__.items()
    },
)


class ExperimentPatch(ExperimentUpdate):
    skip_answers_generation: bool = False


#
# Experiment Set
#


class ExperimentSetBase(EgBaseModel):
    name: str
    readme: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ExperimentSetCreate(ExperimentSetBase):
    def to_table_init(self, db: Session) -> dict:
        obj = self.recurse_table_init(db)
        return {**obj}


class ExperimentSet(ExperimentSetBase):
    id: int
    created_at: datetime
    experiments: list[Experiment] | None


ExperimentSetUpdate = create_model(
    "ExperimentSet",
    **{
        field_name: (Optional[field], None)
        for field_name, field in ExperimentSet.__annotations__.items()
    },
)
