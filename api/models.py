from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base

# By convention, we reserve the String type for Enum defined in the schema scope.


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    type_ = Column(String)

class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    prompt_system = Column(String)
    prompt_template = Column(String)
    sampling_params = Column(JSON)  # dict
    extra_kw = Column(JSON)  # dict


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    metric = Column(String)
    status = Column(String)
    score = Column(JSON)  # dataframe
    generation_table = Column(JSON)  # list of dict

    experiment_id = Column(Integer, ForeignKey("experiments.id"))



class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    metrics = Column(JSON)  # list of enum

    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    dataset = relationship("Dataset")
    model_id = Column(Integer, ForeignKey("models.id"))
    model = relationship("Model")
    experiment_set_id = Column(Integer, ForeignKey("experiment_sets.id"))
    experiment_set = relationship("ExperimentSet")
    results = relationship("Result")


class ExperimentSet(Base):
    __tablename__ = "experiment_sets"

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    created_at = Column(DateTime, server_default=func.now())

    experiments = relationship("experiment")
