from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import RelationshipProperty, class_mapper, declarative_base, relationship
from sqlalchemy.sql import func

import evalap.api.schemas as schemas

Base = declarative_base()


# By convention, we reserve the String type for Enum defined in the schema scope.
#
def is_equal(model1, model2) -> bool:
    """Check if two data model are equal,
    Either they come from a model, a schema or a dict

    Note: This os a lazy check; we ignore model ID field, and hidden fileds like api_key...
          In fact, we check the "Create" version of the schema, eventually by doing a schema regression.
          See the judge_model equality usage to ensure patch route behavior.
    """
    if model1 == model2:
        return True

    data = []
    for v in (model1, model2):
        if isinstance(v, schemas.EgBaseModel):
            # Schema
            value = v.model_dump()
        elif isinstance(v, Base):
            # Model (sql)
            model_class_name = v.__class__.__name__
            # Try to find the schema class
            if hasattr(schemas, model_class_name):
                if hasattr(schemas, model_class_name + "Create"):
                    schema_class = getattr(schemas, model_class_name + "Create")
                else:
                    schema_class = getattr(schemas, model_class_name)
                value = schema_class.model_validate(v).model_dump()
            else:
                raise ValueError(f"No schema found for model {model_class_name}")
        elif isinstance(v, dict):
            # Raw dict
            value = v.copy()
        else:
            raise ValueError(f"Unknown type for data {type(v)}")

        data.append(value)

    # Remove special and hidden attributes
    special_attrs = ["id", "api_key"]
    data = [{k: v for k, v in d.items() if k not in special_attrs} for d in data]

    return all(d == data[0] for d in data)


def is_relationship(model, attribute_name):
    mapper = class_mapper(model)
    property = mapper.attrs.get(attribute_name)
    return isinstance(property, RelationshipProperty)


def create_object_from_dict(db, model, data):
    """Create a SQL object from a nested dictionary with relationship"""
    if isinstance(data, Base):
        return data

    # Separate relationships from simple attributes
    relationships = {}
    attributes = {}
    for k, v in data.items():
        if hasattr(model, k):
            if is_relationship(model, k):
                if v is None:
                    continue
                relationships[k] = v
            else:
                attributes[k] = v

    # Create the main object
    obj = model(**attributes)

    # Handle relationships
    for rel_name, rel_data in relationships.items():
        rel_model = getattr(model, rel_name).property.mapper.class_
        if isinstance(rel_data, Base):  # Relationship is already a db model
            setattr(obj, rel_name, rel_data)
        elif isinstance(rel_data, list):  # Handle one-to-many or many-to-many
            related_objs = [create_object_from_dict(db, rel_model, item) for item in rel_data]
            setattr(obj, rel_name, related_objs)
        elif isinstance(rel_data, (dict, schemas.EgBaseModel)):  # Handle one-to-one or many-to-one
            if isinstance(rel_data, schemas.EgBaseModel):
                rel_data = vars(rel_data)
            related_obj = create_object_from_dict(db, rel_model, rel_data)
            setattr(obj, rel_name, related_obj)
        else:
            raise NotImplementedError(f"Unknonw type for relationtioship {rel_name}:{type(rel_data)}")

    return obj


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    name = Column(Text, unique=True)
    readme = Column(Text)
    default_metric = Column(Text)
    columns_map = Column(JSON)  # dict[str, str]
    df = Column(JSON)  # df
    size = Column(Integer)  # rows
    columns = Column(JSON)  # list[str]
    parquet_path = Column(Text)
    parquet_size = Column(Integer)  # rows
    parquet_columns = Column(JSON)  # list[str]
    parquet_byte_size = Column(Integer)
    compliance = Column(Boolean, default=False)


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    aliased_name = Column(Text)
    base_url = Column(Text)
    api_key = Column(Text)
    system_prompt = Column(Text)
    prelude_prompt = Column(Text)
    # prompt_template = Column(Text) # rag, composition, multiagents ?
    sampling_params = Column(JSON)  # dict
    extra_params = Column(JSON)  # dict
    has_raw_output = Column(Boolean, default=False)


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    metric_name = Column(String)
    metric_aliased_name = Column(String)
    metric_params = Column(JSON)  # dict
    num_try = Column(Integer, default=0)
    num_success = Column(Integer, default=0)
    metric_status = Column(String)

    # One
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    experiment = relationship("Experiment", back_populates="results")
    # Many
    observation_table = relationship("ObservationTable", back_populates="result", cascade="all, delete-orphan")


class ObservationTable(Base):
    __tablename__ = "observation_table"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    score = Column(Float)
    observation = Column(JSON)
    num_line = Column(Integer)
    error_msg = Column(Text)
    execution_time = Column(Integer)
    emission_carbon = Column(JSON)  # dict[ecologits]

    # One
    result_id = Column(Integer, ForeignKey("results.id"))
    result = relationship("Result", back_populates="observation_table")

    __table_args__ = (UniqueConstraint("num_line", "result_id", name="_metric_num_line_unique_constraint"),)


class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    answer = Column(Text)
    think = Column(Text)
    num_line = Column(Integer)
    error_msg = Column(Text)
    execution_time = Column(Integer)
    nb_tokens_prompt = Column(Integer)
    nb_tokens_completion = Column(Integer)
    nb_tool_calls = Column(Integer)
    context = Column(JSON)  # list[str]
    retrieval_context = Column(JSON)  # list[str]
    tool_steps = Column(JSON)  # list[list[dict]]
    emission_carbon = Column(JSON)  # dict[ecologits]

    # One
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    experiment = relationship("Experiment", back_populates="answers")

    __table_args__ = (
        UniqueConstraint("num_line", "experiment_id", name="_answer_num_line_unique_constraint"),
    )


class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    readme = Column(Text)
    is_archived = Column(Boolean, default=False)  # do not allow user to remove without IAM.
    created_at = Column(DateTime, server_default=func.now())
    experiment_status = Column(String)
    with_vision = Column(Boolean)
    sample = Column(JSON)  # list[int]
    num_try = Column(Integer, default=0)
    num_success = Column(Integer, default=0)

    @property
    def num_observation_try(self):
        return sum(result.num_try for result in self.results)

    @property
    def num_observation_success(self):
        return sum(result.num_success for result in self.results)

    @property
    def num_metrics(self):
        return len(self.results)

    # One
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    dataset = relationship("Dataset")
    model_id = Column(Integer, ForeignKey("models.id"))
    model = relationship("Model", foreign_keys=[model_id], cascade="all, delete-orphan", single_parent=True)
    judge_model_id = Column(Integer, ForeignKey("models.id"))
    judge_model = relationship("Model", foreign_keys=[judge_model_id], cascade="all, delete")
    experiment_set_id = Column(Integer, ForeignKey("experiment_sets.id"))
    experiment_set = relationship("ExperimentSet", back_populates="experiments")
    # Many
    results = relationship("Result", back_populates="experiment")  # len == #metrics
    answers = relationship("Answer", back_populates="experiment")  # len == #dataset.df

    __table_args__ = (UniqueConstraint("experiment_set_id", "name", name="_expset_name_unique_constraint"),)


class ExperimentSet(Base):
    __tablename__ = "experiment_sets"

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    readme = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    is_archived = Column(Boolean, default=False)  # do not allow user to remove without IAM.

    # Many
    experiments = relationship("Experiment", back_populates="experiment_set")


#
# LOCUST
#


class LocustRun(Base):
    __tablename__ = "locustrun"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    scenario = Column(Text)
    model = Column(Text)
    api_url = Column(Text)
    stats_df = Column(Text)
    history_df = Column(Text)
    custom_history_df = Column(Text)


#
# Load testing
#


class LoadTesting(Base):
    __tablename__ = "loadtesting"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    model = Column(Text)
    name = Column(Text)
    prompt = Column(Text)
    df = Column(JSON)  # df
