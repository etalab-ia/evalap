from . import metric_registry


@metric_registry.register(
    name="output_length",
    description="Binary correspondance between output and output_true",
    metric_type="llm",
    require=["output"],
)
def output_length_metric(output, *args, **kwargs):
    return len(output.split())
