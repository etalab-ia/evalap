from . import metric_registry


@metric_registry.register(
    name="qcm_exactness",
    description="[0;1] La métrique 'qcm_exactness' vérifie simplement si la réponse donnée à une question à choix multiple (QCM) est exactement égale à la bonne réponse attendue. Elle retourne 1 pour une correspondance parfaite, sinon 0, permettant de valider la justesse binaire des réponses aux QCM. Cette métrique est à utiliser uniquement pour des cas d'usage de QCM",
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
