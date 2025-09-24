from evalap.clients import LlmClient, split_think_answer
from evalap.utils import render_jinja

from . import metric_registry

_template = """
Analysez la question, la réponse standard et la réponse d'un autre agent fournie ci-dessous. Votre tâche est d'évaluer les DIVAGATIONS dans la réponse de l'autre agent, c'est-à-dire le contenu non pertinent ou hors sujet.

Question posée :

<A>
{{query}}
</A>


Réponse standard (LA REFERENCE!) :

<B>
{{output_true}}
</B>


Réponse générée par un autre agent à évaluer :

<C>
{{output}}
</C>


Instructions :
    1. Identifiez le contenu de la réponse de l'autre agent qui n'est pas directement lié à la question ou qui n'apporte pas d'information essentielle.
    2. Évaluez la proportion de ce contenu non pertinent dans la réponse de l'autre agent.
    3. Attribuez une note de 1 à 10 pour les divagations :
    - 1 : Aucune divagation, réponse entièrement pertinente
    - 10 : Majoritairement des divagations, peu de contenu pertinent

Répondez UNIQUEMENT avec la note (ET RIEN D AUTRE) sous ce format :
NOTE
""".strip()

_config = {
    "model": "gpt-4o",
    # "system_prompt": "Tu donnes...."
    "sampling_params": {"temperature": 0.2},
}


@metric_registry.register(
    name="judge_rambling",
    description="[1-10] The 'judge_rambling' metric measures the amount of irrelevant or off-topic content in a response relative to the question asked. It assigns a score from 1 (completely relevant response) to 10 (mostly off-topic response), helping to detect and limit rambling in AI agent responses.",
    metric_type="llm",
    require=["output", "output_true", "query"],
)
def judge_pertinence_metric(output, output_true, **kwargs):
    config = _config | {k: v for k, v in kwargs.items() if k in _config}
    messages = [
        {
            "role": "user",
            "content": render_jinja(_template, output=output, output_true=output_true, **kwargs),
        }
    ]
    model = config["model"]
    aiclient = LlmClient(base_url=model.base_url, api_key=model.api_key)
    result = aiclient.generate(model=model.name, messages=messages, **config["sampling_params"])
    observation = result.choices[0].message.content
    think, answer = split_think_answer(observation)
    score = answer.strip(" \n\"'.%")
    try:
        score = float(score)
    except ValueError:
        score = None
    return score, observation, result
