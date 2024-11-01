from . import metric_registry


@metric_registry.register(name="qcm_exactness", metric_type="llm", require=["output", "output_true"])
def qcm_metric(output, output_true, **kwargs):
    pass
