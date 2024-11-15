from . import metric_registry

@metric_registry.register(
    name="nb_tokens_prompt",
    description="Number of tokens in the prompt",
    metric_type="llm",
    require=["query"],
)
def nb_tokens_prompt_metric(output, *args, **kwargs):
    metadata = kwargs["metadata"]
    return metadata.get("nb_tokens_prompt")

@metric_registry.register(
    name="nb_tokens_completion",
    description="Number of tokens in the completion",
    metric_type="llm",
    require=["query"],
)
def nb_tokens_completion_metric(output, *args, **kwargs):
    metadata = kwargs["metadata"]
    return metadata.get("nb_tokens_completion")


@metric_registry.register(
    name="generation_time",
    description="The time to generate the answer/output",
    metric_type="llm",
    require=["query"],
)
def generation_time_metric(output, *args, **kwargs):
    metadata = kwargs["metadata"]
    return metadata.get("generation_time")
