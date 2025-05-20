from . import metric_registry
import logging
from eg1.logger import logger


@metric_registry.register(
    name="nb_tokens_prompt", description="Number of tokens in the prompt", metric_type="ops", require=["query"]
)
def nb_tokens_prompt_metric(output, *args, **kwargs):
    metadata = kwargs["metadata"]
    return metadata.get("nb_tokens_prompt")


@metric_registry.register(
    name="nb_tokens_completion",
    description="Number of tokens in the completion",
    metric_type="ops",
    require=["output"],
)
def nb_tokens_completion_metric(output, *args, **kwargs):
    metadata = kwargs["metadata"]
    return metadata.get("nb_tokens_completion")


@metric_registry.register(
    name="nb_tool_calls",
    description="Number of tools that has been called for the generation",
    metric_type="ops",
    require=["output"],
)
def nb_tool_calls_metric(output, *args, **kwargs):
    metadata = kwargs["metadata"]
    return metadata.get("nb_tool_calls")


@metric_registry.register(
    name="generation_time",
    description="The time to generate the answer/output",
    metric_type="ops",
    require=["output"],
)
def generation_time_metric(output, *args, **kwargs):
    metadata = kwargs["metadata"]
    logging.info("metadata >>>>> ")
    logging.info(metadata)

    return metadata.get("generation_time")


def average_metric_from_emission_carbon(emission_carbon, key):
    """
    Calcule la moyenne (min+max)/2 pour la sous-catégorie donnée (key)
    dans le dictionnaire emission_carbon.
    """
    item = emission_carbon.get(key)
    if not item:
        return None
    value = item.get("value")
    if not value or not isinstance(value, dict):
        return None
    min_val = value.get("min")
    max_val = value.get("max")
    if min_val is None or max_val is None:
        return None
    return (min_val + max_val) / 2


@metric_registry.register(
    name="energy_consumption",
    description="Energy consumption (kWh) - Environmental impact calculated by librairy ecologits",
    metric_type="ops",
    require=["output"],
)
def energy_consumption_metric(output, *args, **kwargs):
    emission_carbon = kwargs["metadata"].get("emission_carbon", {})
    return average_metric_from_emission_carbon(emission_carbon, "energy")


@metric_registry.register(
    name="gwp_consumption",
    description=" Global Warming Potential (kgCO2eq) - Environmental impact calculated by librairy ecologits",
    metric_type="ops",
    require=["output"],
)
def gwp_metric(output, *args, **kwargs):
    emission_carbon = kwargs["metadata"].get("emission_carbon", {})
    return average_metric_from_emission_carbon(emission_carbon, "gwp")
