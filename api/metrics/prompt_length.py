from . import metric_registry


@metric_registry.register(name="prompt_length", metric_type="llm", require=["output"])
def prompt_length_metric(output, *args, **kwargs):
    return len(output.split())
