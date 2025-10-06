from datetime import datetime
from enum import Enum
from io import StringIO
from typing import Any, Literal, Optional

import numpy as np
import pandas as pd
from pydantic import BaseModel, ConfigDict, Field, create_model
from sqlalchemy.orm import Session

import evalap.api.models as models
from evalap.api.errors import SchemaError
from evalap.api.metrics import metric_registry
from evalap.clients.llm import LlmApiModels, get_api_url
from evalap.utils import build_param_grid

# @WARNING: this is a raw copy of the evalap.api.schema.py !

#
# Custom BaseModel
#
class EgBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        protected_namespaces=(),
        json_encoders={
            # np.nan is not serializable !
            float: lambda v: None if np.isnan(v) else v,
        },
        extra="forbid",  # Do not allow unknow field
    )

    def recurse_table_init(self, db: Session) -> dict:
        obj = self.model_dump()
        for k, v in obj.items():
            sub_schema = getattr(self, k)
            if hasattr(sub_schema, "to_table_init"):
                obj[k] = sub_schema.to_table_init(db)
            elif isinstance(sub_schema, list):
                obj[k] = [o.to_table_init(db) if isinstance(o, EgBaseModel) else o for o in sub_schema]

        return obj

    def to_table_init(self, db: Session):
        return self.model_dump()


#
# Metrics
#

MetricEnum = Enum("MetricEnum", {name: name for name in metric_registry.get_metric_names()}, type=str)


class MetricParametrized(BaseModel):
    name: str
    params: dict | None = None
    aliased_name: str | None = None


class ExperimentStatus(str, Enum):
    pending = "pending"
    running_answers = "running_answers"
    running_metrics = "running_metrics"
    finished = "finished"


class MetricStatus(str, Enum):
    pending = "pending"
    running = "running"
    finished = "finished"


#
# Dataset
#


class DatasetBase(EgBaseModel):
    name: str
    readme: str
    default_metric: str
    columns_map: dict[str, str] | None = Field(
        None,
        description="A column names maping that indicates what names in dataset match the evalap stadandard (output, output_true etc)",
    )


class DatasetCreate(DatasetBase):
    df: str  # from_json

    def to_table_init(self, db: Session) -> dict:
        obj = self.recurse_table_init(db)

        # Handle dataframe
        try:
            df = pd.read_json(StringIO(self.df))
        except ValueError:
            raise SchemaError("'df' should be a readable dataframe. Use df.to_json()...")

        return {
            "size": len(df),
            "columns": list(df.columns),
            "parquet_size": 0,
            "parquet_columns": [],
            **obj,
        }


class Dataset(DatasetBase):
    id: int
    created_at: datetime
    size: int = Field(description="Number of rows in the dataset (length of the dataframe)")
    columns: list[str]
    parquet_size: int = Field(description="Number of rows in the dataset (length of the parquet file)")
    parquet_columns: list[str]


class DatasetFull(Dataset):
    df: str  # from_json


DatasetUpdate = create_model(
    "DatasetUpdate",
    **{field_name: (Optional[field.annotation], None) for field_name, field in Dataset.model_fields.items()},
    __base__=Dataset,
)


# Do not allow to update the content of a dataset to prevent breaking
# expriment alignement with num_line
DatasetPatch = create_model(
    "DatasetPatch",
    **{field_name: (Optional[field.annotation], None) for field_name, field in Dataset.model_fields.items()},
    __base__=DatasetBase,
)

#
# Model
#


class ModelBase(EgBaseModel):
    name: str
    base_url: str
    aliased_name: str | None = None
    system_prompt: str | None = None
    prelude_prompt: str | None = None
    sampling_params: dict | None = None
    extra_params: dict | None = None


class ModelCreate(ModelBase):
    api_key: str


class Model(ModelBase):
    id: int
    has_raw_output: bool = False


class ModelWithKeys(Model):
    api_key: str


class ModelRaw(EgBaseModel):
    # Answers
    output: list[str] = Field(
        description="The sequence of answers generated for this model, ordered as the 'rows' input of the dataset you are working on."
    )
    # ModelBase
    aliased_name: str = Field(
        description="A name to identify this model. The difference with the `name` parameter is that the latter must be used to identify the model name in the Openai API-compatible endpoint."
    )
    name: str = ""
    base_url: str = ""
    system_prompt: str | None = None
    prelude_prompt: str | None = None
    sampling_params: dict | None = None
    extra_params: dict | None = None
    # Ops metrics
    execution_time: list[int] | None = None
    nb_tokens_prompt: list[int] | None = None
    nb_tokens_completion: list[int] | None = None
    nb_tool_calls: list[int] | None = None
    context: list[list[str]] | None = None
    retrieval_context: list[list[str]] | None = None
    think: list[str] | None = None


#
# Result
#


class Answer(EgBaseModel):
    id: int
    created_at: datetime
    answer: str | None
    think: str | None
    context: list[str] | None
    retrieval_context: list[str] | None
    num_line: int
    error_msg: str | None
    execution_time: int | None
    tool_steps: list | None


class AnswerWithEco(Answer):
    """Answer with emission_carbon field for eco metrics."""

    emission_carbon: dict | None


class Observation(EgBaseModel):
    id: int
    created_at: datetime
    score: float | None
    observation: str | dict | list | None  # json
    num_line: int
    error_msg: str | None
    execution_time: int | None


class ResultBase(EgBaseModel):
    metric_name: MetricEnum
    metric_params: dict | None = None
    metric_aliased_name: str | None = None


class ResultCreate(ResultBase):
    experiment_id: int | None = None

    def to_table_init(self, db):
        obj = self.recurse_table_init(db)
        return {"metric_status": "pending", **obj}


class Result(ResultBase):
    id: int
    created_at: datetime
    observation_table: list[Observation]
    num_try: int
    num_success: int
    experiment_id: int
    metric_status: MetricStatus


ResultUpdate = create_model(
    "ResultUpdate",
    **{field_name: (Optional[field.annotation], None) for field_name, field in Result.model_fields.items()},
    __base__=Result,
)

#
# Experiment
#


class ExperimentBase(EgBaseModel):
    name: str
    readme: str | None = None
    experiment_set_id: int | None = None
    judge_model: ModelCreate | Literal[*LlmApiModels._all_models()] | None = None
    with_vision: bool = Field(
        False,
        description="Add the image to the user message if an 'img' field is present in the dataset (parquet).",
    )


class ExperimentCreate(ExperimentBase):
    metrics: list[MetricEnum | MetricParametrized]
    dataset: DatasetCreate | str
    model: ModelCreate | ModelRaw

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
        if isinstance(self.model, ModelRaw):
            obj["num_try"] = dataset.parquet_size if self.with_vision else dataset.size
            obj["num_success"] = len(self.model.output)
            if obj["num_try"] != obj["num_success"]:
                raise SchemaError("The size of the model outputs must match the size of the dataset.")

        # Handle Model
        has_raw_output = False
        if isinstance(self.model, ModelRaw):
            model = {k: v for k, v in self.model.model_dump().items() if k in ModelCreate.model_fields}
            has_raw_output = True
            model["has_raw_output"] = has_raw_output
            # Create Answers from ModelRaw
            # --
            answers = []
            m = self.model
            df = pd.read_json(StringIO(dataset.df))
            if len(df) != len(m.output):
                raise SchemaError("The size of the model outputs must match the size of the dataset.")

            for i in range(len(m.output)):
                answers.append(
                    dict(
                        num_line=i,
                        answer = m.output[i],
                        think=m.think[i] if m.think else None,
                        execution_time=m.execution_time[i] if m.execution_time else None,
                        nb_tokens_prompt=m.nb_tokens_prompt[i] if m.nb_tokens_prompt else None,
                        nb_tokens_completion=m.nb_tokens_completion[i] if m.nb_tokens_completion else None,
                        nb_tool_calls=m.nb_tool_calls[i] if m.nb_tool_calls else None,
                        context=m.context[i] if m.context else None,
                        retrieval_context=m.retrieval_context[i] if m.retrieval_context else None,
                    )
                )  # fmt: skip
            obj["answers"] = answers
        else:
            model = self.model
        obj["model"] = model

        # Handle judge_model
        if isinstance(self.judge_model, str):
            url, headers = get_api_url(self.judge_model)
            obj["judge_model"] = ModelCreate(
                **{
                    "name": self.judge_model,
                    "base_url": url,
                    "api_key": (headers.get("Authorization") or headers.get("x-api-key") or "").split()[-1],
                }
            ).model_dump()

        # Handle Metrics Results
        results = []
        for metric in self.metrics:
            if isinstance(metric, str):
                metric_name = metric
                metric_params = None
            else:
                metric_name = metric.name
                metric_params = metric.params

            results.append(
                ResultCreate(metric_name=metric_name, metric_params=metric_params).to_table_init(db)
            )

            # Validate Model and metric compatibility
            # --
            DEBUG_EXCEPTION_REQUIRE = [
                "output",
                "context",
                "retrieval_context",
            ]  # fetch at runtime with tooling
            metric_obj = metric_registry.get_metric(metric_name)
            # Check require fields
            required_args = metric_obj.require
            if not required_args and "prompt" in (metric_params or {}):
                required_args = metric_registry.get_require_from_prompt_tempalte(metric_params["prompt"])

            for require in required_args:
                if require in DEBUG_EXCEPTION_REQUIRE:
                    continue
                if require not in (dataset.columns + dataset.parquet_columns):
                    if dataset.columns_map and dataset.columns_map.get(require) in (
                        dataset.columns + dataset.parquet_columns
                    ):
                        # Handle columns_maps
                        continue
                    raise SchemaError(
                        f"Metric {metric_name} require a parameter `{require}`. "
                        f"Either your dataset needs to have a `{require}` field or use ModelRaw schema to provide it yourself if its a model generated field."
                    )

            # Check metric params
            if not isinstance(metric, str) and metric_params:
                params = set(metric_params)
                valid_params = set(metric_obj.required_params or []) | set(metric_obj.optional_params or [])
                invalid_params = params - valid_params
                if invalid_params:
                    raise SchemaError(
                        f"Invalid parameters for metric '{metric_name}': {invalid_params}. "
                        f"Valid parameters are: {valid_params}"
                    )
            elif metric_obj.required_params:
                raise SchemaError(
                    f"Metric '{metric_name}' has required parameters {metric_obj.required_params} but none were provided. "
                    f"Use dict format to specify parameters."
                )

        obj["results"] = results
        return {
            "experiment_status": "pending",
            **obj,
        }


class Experiment(ExperimentBase):
    id: int
    created_at: datetime
    experiment_status: ExperimentStatus
    num_try: int = Field(description="How many output/answers were attempted to be generated.")
    num_success: int = Field(description="How many output/answers were successfully generated.")
    num_observation_try: int = Field(
        description="How many metric observations were attempted to be generated."
    )
    num_observation_success: int = Field(
        description="How many metric observations were successfully generated."
    )
    num_metrics: int = Field(
        description="How many metrics are associated to this experiment. See the query parameter `with_results` to get the results per metrics."
    )

    dataset: Dataset
    model: Model | None
    judge_model: Model | None


class ExperimentWithResults(Experiment):
    results: list[Result] | None


class ExperimentWithAnswers(Experiment):
    answers: list[Answer] | None


class ExperimentFull(Experiment):
    answers: list[Answer] | None = None
    results: list[Result] | None = None


class ExperimentFullWithDataset(ExperimentFull):
    dataset: DatasetFull | None = None


class ExperimentFullWithEco(ExperimentFull):
    answers: list[AnswerWithEco] | None


# For the special `metrics` paramter passed at creation
class ExperimentExtra(Experiment, ExperimentCreate):
    pass


ExperimentUpdate = create_model(
    "ExperimentUpdate",
    **{
        field_name: (Optional[field.annotation], None)
        for field_name, field in ExperimentExtra.model_fields.items()
    },
    __base__=ExperimentExtra,
)


class ExperimentPatch(ExperimentUpdate):
    rerun_answers: bool = False


#
# Experiment Set
#


class GridCV(BaseModel):
    common_params: dict[str, Any]
    grid_params: dict[str, list[Any]]
    repeat: int = 1


class ExperimentSetBase(EgBaseModel):
    name: str
    readme: str


class ExperimentSetCreate(ExperimentSetBase):
    experiments: list[ExperimentCreate] | None = None
    cv: GridCV | None = None

    def to_table_init(self, db: Session, expe_size: int = 0) -> dict:
        obj = self.recurse_table_init(db)

        if self.experiments is not None and self.cv is not None:
            raise SchemaError("Please, give either an expriments or a cv parameter but not both.")

        # Handle Experiments
        if self.cv is not None:
            experiments = []
            i = expe_size
            for experiment in build_param_grid(self.cv.common_params, self.cv.grid_params):
                for _ in range(self.cv.repeat):
                    experiment["name"] = f"{self.name}__{i}"
                    experiments.append(ExperimentCreate(**experiment).to_table_init(db))
                    i += 1
            obj["experiments"] = experiments
        elif self.experiments is None:
            obj.pop("experiments")

        # Ensure judge_model are all equal
        if obj.get("experiments"):
            if len(set([x["judge_model"]["name"] for x in obj["experiments"] if x["judge_model"]])) > 1:
                raise SchemaError("The juge_model must be the same for all experiments in a set.")

        return obj


class ExperimentSet(ExperimentSetBase):
    id: int
    created_at: datetime
    experiments: list[Experiment] | None


# For the special `cv` parameters passed at creation
class ExperimentSetExtra(ExperimentSet, ExperimentSetCreate):
    experiments: list[Experiment | ExperimentCreate] | None


ExperimentSetUpdate = create_model(
    "ExperimentSetUpdate",
    **{
        field_name: (Optional[field.annotation], None)
        for field_name, field in ExperimentSet.model_fields.items()
    },
    __base__=ExperimentSetExtra,
)


class ExperimentSetPatch(ExperimentSetUpdate):
    experiments: list[Experiment | ExperimentCreate] | None = None


class RetryRuns(EgBaseModel):
    # List of experiment to retry
    experiment_ids: list[int]
    # List of results/metrics to retry
    result_ids: list[int]
    # List of unfinished experiments to process
    unfinished_experiment_ids: list[int]
    # List of unfinished results to process
    unfinished_result_ids: list[int]


#
# LeaderBoard
#


class LeaderboardEntry(BaseModel):
    experiment_id: int
    experiment_name: str
    model_name: str
    dataset_name: str
    main_metric_score: Optional[float]
    other_metrics: dict
    system_prompt: Optional[str] = None
    sampling_param: dict
    extra_param: dict
    created_at: datetime
    experiment_set_id: Optional[int] = None
    experiment_set_name: Optional[str] = None
    judge_model: Optional[str | dict] = None


class Leaderboard(EgBaseModel):
    entries: list[LeaderboardEntry]


#
# Ops
#


class ModelInfo(BaseModel):
    name: str
    aliased_name: Optional[str]


class OpsMetrics(BaseModel):
    experiment_sets: int
    unique_experiments: int
    unique_answers: int
    unique_metrics: int
    unique_observations: int
    distinct_models: list[ModelInfo]


class OpsEcoDetails(BaseModel):
    total_emissions: dict[str, float]
    total_entries_with_emissions: int
    first_emission_date: datetime | None


class OpsEcoGlobal(BaseModel):
    answers: OpsEcoDetails
    observation_table: OpsEcoDetails


#
# LOCUST
#


class LocustRunBase(EgBaseModel):
    scenario: str = Field(..., description="The locust scenario name.")
    model: str | None = Field(None, description="The LLM model name/id targeted if any.")
    api_url: str = Field(..., description="The url targeted.")


class LocustRunCreate(LocustRunBase):
    stats_df: str = Field(..., description="The stats csv file serialized as a dataframe.")
    history_df: str = Field(..., description="The stats history CSV file serialized as a dataframe.")
    custom_history_df: str | None = Field(None, description="Extra stats history serialized as a dataframe.")


class LocustRun(LocustRunBase):
    id: int
    created_at: datetime


class LocustRunFull(LocustRun):
    stats_df: str = Field(..., description="The stats csv file serialized as a dataframe.")
    history_df: str = Field(..., description="The stats history CSV file serialized as a dataframe.")
    custom_history_df: str | None = Field(None, description="Extra stats serialized as a dataframe.")


#
# Load Testing
#


class LoadTestingBase(EgBaseModel):
    model: str | None = Field(None, description="The LLM model name/id targeted if any.")
    name: str | None = Field(None, description="The name of the run.")
    prompt: str | None = Field(None, description="The prompt use for the run.")


class LoadTestingCreate(LoadTestingBase):
    df: str = Field(..., description="The stats data.")  # from_json


class LoadTesting(LoadTestingBase):
    id: int
    created_at: datetime


class LoadTestingFull(LoadTesting):
    df: str = Field(..., description="The stats data.")  # from_json
