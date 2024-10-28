from dataclasses import dataclass
from enum import Enum


class MetricType(str, Enum):
    deepeval = "deepeval"
    adhoc = "adhoc"
    human = "human"


@dataclass
class Metric:
    name: str
    type_: MetricType


all_metrics = [
    {
        "name": "qcm",
        "type_": MetricType.adhoc,
        "require": ["answer", "answer_true"]
    },
    {
        "name": "human-vote",
        "type_": MetricType.human,
        "require": ["answer"]
    },
    {
        "name": "g",
        "type_": MetricType.deepeval,
        "require": ["answer"]
    },
    {
        "name": "blue",
        "type_": MetricType.deepeval,
        "require": []
    },
]


all_metrics = {d["name"]: d for d in all_metrics}
all_metrics_names = list(all_metrics.keys())
