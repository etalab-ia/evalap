from . import metric_registry


@metric_registry.register(
    name="qcm_exactness",
    description="[0;1] The 'qcm_exactness' metric simply checks whether the answer given to a multiple-choice question (MCQ) is exactly equal to the expected correct answer. It returns 1 for a perfect match, otherwise 0, allowing you to validate the binary accuracy of MCQ answers. This metric should only be used for MCQ use cases.",
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
