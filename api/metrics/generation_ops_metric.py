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