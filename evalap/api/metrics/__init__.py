import importlib
import os
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Union

import inflection
from deepeval.key_handler import KEY_FILE_HANDLER
from deepeval.models.base_model import DeepEvalBaseLLM

from evalap.clients import LlmClient, get_api_url, split_think_answer
from evalap.utils import import_classes

# FIX deepeval: OSError: [Errno 24] Too many open files: '.deepeval'
KEY_FILE_HANDLER.fetch_data = lambda x: None

if TYPE_CHECKING:
    import evalap.api.models as models
    import evalap.api.schemas as schemas


def get_judge_model(model: Union[str, "models.Model"]) -> "schemas.ModelCreate":
    import evalap.api.models as models
    import evalap.api.schemas as schemas

    if isinstance(model, models.Base):
        model = schemas.ModelCreate.model_validate(model)
    elif isinstance(model, str):
        url, headers = get_api_url(model)
        model = schemas.ModelCreate(
            name=model,
            base_url=url,
            api_key=(headers.get("Authorization") or headers.get("x-api-key") or "").split()[-1],
        )
    else:
        raise ValueError("Model type for judge unsuported.")

    return model


class MetricType(str, Enum):
    # @TODO: ill defined at this point...
    llm = "llm"  # query:str, output:str
    deepeval = "deepeval"
    human = "human"


@dataclass
class Metric:
    name: str
    description: str
    type: MetricType
    require: list[str]

    @classmethod
    def from_dict(cls, d: dict):
        return cls(**{k: v for k, v in d.items() if k not in ["func"]})


class CustomModel(DeepEvalBaseLLM):
    def __init__(self, model: "models.Model"):
        self._model = model

    def load_model(self):
        # @DEBUG: is it depeval "compatibble" ?
        return self._model

    def get_model_name(self) -> str:
        return self._model.name

    def generate(self, prompt: str) -> str:
        model = self._model
        system_prompt = model.system_prompt or "Answer in JSON format stricly."
        sampling_params = model.sampling_params or {}
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages
        aiclient = LlmClient(base_url=model.base_url, api_key=model.api_key)
        result = aiclient.generate(model=model.name, messages=messages, **sampling_params)
        observation = result.choices[0].message.content
        think, answer = split_think_answer(observation)
        return answer

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)


class MetricRegistry:
    deepeval_require_map = {
        "input": "query",
        "actual_output": "output",
        "expected_output": "output_true",
        "context": "context",
        "retrieval_context": "retrieval_context",
        "reasoning": "reasoning",
        # "tools_called": "tools",
        # "expected_tools": "tools_true",
    }

    def __init__(self):
        self._metrics = {}

    def register(self, name: str, description: str, metric_type: str, require: list[str]):
        def decorator(func):
            self._metrics[name] = {
                "name": name,
                "description": description,
                "type": metric_type,
                "require": sorted(require),
                "func": func,
            }
            return func

        return decorator

    def register_deepeval(self, metric_class, name, description, required_params):
        from deepeval.test_case import LLMTestCase

        require = [self.deepeval_require_map[k.value] for k in required_params or []]
        reverse_require_map = {v: k for k, v in self.deepeval_require_map.items()}

        def wrapped_metric(output, output_true=None, **metric_params):
            # Metric computation
            model = CustomModel(metric_params["model"])
            metric = metric_class(model=model)
            test_case = LLMTestCase(
                **{
                    reverse_require_map[k]: v
                    for k, v in ({"output": output, "output_true": output_true} | metric_params).items()
                    if k in reverse_require_map
                }
            )
            try:
                metric.measure(test_case, _show_indicator=False)
            except TypeError:  # External metric, like RAGAS does not have _show_indicator attr
                metric.measure(test_case)

            if hasattr(metric, "reason"):
                return metric.score, metric.reason, None
            return metric.score

        self._metrics[name] = {
            "name": name,
            "description": description,
            "type": "deepeval",
            "require": sorted(require),
            "func": wrapped_metric,
        }

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

# Registed decorated metrics in api.metrics
# --
metrics_package = "evalap.api.metrics"
metrics_directory = __path__[0]
for filename in os.listdir(metrics_directory):
    if filename.endswith(".py") and not filename.startswith("_"):
        # The metric is registed from the decorator @metric_registry.register
        module_name = filename[:-3]
        importlib.import_module(f"{metrics_package}.{module_name}")

# Register some DeepEval metrics
# --
package_name = "deepeval.metrics"
classes = [
    "AnswerRelevancyMetric",
    "FaithfulnessMetric",
    "BiasMetric",
    "ToxicityMetric",
    "HallucinationMetric",
    # Rag metric (required retrieval_context)
    "ContextualPrecisionMetric",
    "ContextualRecallMetric",
    "ContextualRelevancyMetric",
    "RagasMetric",
]
more = ["required_params"]
imported_objs = import_classes(package_name, classes, more=more)
for class_name, obj in zip(classes, imported_objs):
    if not obj:
        continue

    name = inflection.underscore(class_name.replace("Metric", ""))
    description = "see https://docs.confident-ai.com/docs/metrics-introduction"
    required_params = obj.get("required_params") or getattr(obj["obj"], "_required_params", None)

    # @DEBUG: Deepeval:RagasMetric does not have the required_params attribute set.
    if class_name == "RagasMetric":
        required_params = Enum("_", {name: name for name in ["input", "expected_output", "retrieval_context"]})

    metric_registry.register_deepeval(
        metric_class=obj["obj"],
        name=name,
        description=description,
        required_params=required_params,
    )
