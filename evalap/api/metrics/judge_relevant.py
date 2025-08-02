from evalap.clients import LlmClient, split_think_answer
from evalap.utils import render_jinja

from . import metric_registry, get_judge_model

_template = """
Analysez la question, la réponse standard et la réponse d'un autre agent fournie ci-dessous. Votre tâche est d'évaluer la PERTINENCE de la réponse de l'autre agent par rapport aux éléments essentiels de la réponse standard.

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
1. Identifiez les éléments essentiels dans la réponse standard.
2. Vérifiez si ces éléments sont présents dans la réponse de l'autre agent.
3. Attribuez une note de 1 à 10 pour la pertinence :
- 10 : Tous les éléments essentiels sont présents
- 1 : Aucun élément essentiel n'est présent

Répondez UNIQUEMENT avec la note (ET RIEN D AUTRE) sous ce format :
NOTE
""".strip()

_config = {
    "model": "gpt-4o",
    # "system_prompt": "Tu donnes...."
    "sampling_params": {"temperature": 0.2},
}


@metric_registry.register(
    name="judge_relevant",
    description="[1-10] relevance score between output and output_true",
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
    model = get_judge_model(config["model"])
    aiclient = LlmClient(base_url=model.base_url, api_key=model.api_key)
    result = aiclient.generate(model=model.name, messages=messages, **config["sampling_params"])
    observation = result.choices[0].message.content
    think, answer = split_think_answer(observation)
    score = answer.strip(" \n\"'.%")
    try:
        score = float(score)
    except ValueError:
        score = None
    return score, observation
