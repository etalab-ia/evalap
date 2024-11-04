import importlib
import os
from dataclasses import dataclass
from enum import Enum

# @TODO:
# - Document the signature of a metric function with exemple.
# - Document the signature of the decorator of the register metric.
# - add require to the definition of thje metric (decorator or parsing the sign ?)


class MetricType(str, Enum):
    # @TODO: ill defined at this point...
    deepeval = "deepeval"
    adhoc = "adhoc"
    llm = "llm"
    human = "human"


@dataclass
class Metric:
    name: str
    type: MetricType
    require: list[str]

    @classmethod
    def from_dict(cls, d: dict):
        return cls(**{k: v for k, v in d.items() if k not in ["func"]})


# all_metrics = [
#     {
#         "name": "qcm",
#         "type": MetricType.adhoc,
#         "require": ["answer", "answer_true"]
#     },
#     {
#         "name": "human-vote",
#         "type": MetricType.human,
#         "require": ["answer"]
#     },
#     {
#         "name": "g",
#         "type": MetricType.deepeval,
#         "require": ["answer"]
#     },
#     {
#         "name": "blue",
#         "type": MetricType.deepeval,
#         "require": []
#     },
# ]


class MetricRegistry:
    def __init__(self):
        self._metrics = {}

    def register(self, name: str, metric_type: str, require: list[str]):
        def decorator(func):
            self._metrics[name] = {
                "name": name,
                "type": metric_type,
                "require": require,
                "func": func,
            }
            return func

        return decorator

    def get_metric_function(self, name):
        return self._metrics.get(name, {}).get("func", None)

    def get_metric(self, name) -> Metric:
        return Metric.from_dict(self._metrics.get(name, {}))

    def get_metrics(self) -> list[Metric]:
        return [self.get_metric(name) for name in self._metrics]

    def get_metric_names(self) -> list[str]:
        return list(self._metrics.keys())


# Create a global instance of the MetricRegistry
metric_registry = MetricRegistry()

# Automatically import all metric modules to register them
metrics_directory = __path__[0]
for filename in os.listdir(metrics_directory):
    if filename.endswith(".py") and not filename.startswith("_"):
        module_name = filename[:-3]
        importlib.import_module(f"api.metrics.{module_name}")
