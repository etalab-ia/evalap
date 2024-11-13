from . import metric_registry


@metric_registry.register(
    name="generation_time",
    description="The time to generate the answer/output",
    metric_type="llm",
    require=["query"],
)
def generation_time_metric(output, *args, **kwargs):
    metadata = kwargs["metadata"]
    return metadata.get("generation_time")
