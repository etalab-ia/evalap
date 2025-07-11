from . import metric_registry


@metric_registry.register(
    name="qcm_exactness",
    description="output and output_true binary equality",
    metric_type="llm",
    require=["output", "output_true"],
)
def qcm_metric(output, output_true, **kwargs):
    observation = output.strip(" \n\"'.")
    observation = observation.split()
    if len(observation) > 1:
        return None

    observation = output[0]
    score = 1 if observation == output_true else 0
    return score
