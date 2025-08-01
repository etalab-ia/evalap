from evalap.clients import LlmClient, split_think_answer
from evalap.utils import render_jinja

from . import metric_registry, get_judge_model



_template = """
Vous êtes un assistant IA chargé d'évaluer et de comparer deux textes pour déterminer si le Texte B est plus ou moins similaire (au sens de l'intention) au Texte A, sachant que A est la vérité terrain et B une réponse donnée par un autre LLM.

Texte A (vérité terrain) :

<A>
{{output_true}}
</A>

Texte B (réponse d'un autre LLM) :

<C>
{{output}}
</C>

vous devez fournir une note de complétude indiquant le taux d'intersection entre A et B.
Cette note entre 0 et 100 apparaitera sous la forme (ne surtout pas afficher le %):
 XX

Evidemment pour arriver à ce résultat final vous devez réfléchir à si le Texte B est plus ou moins similaire au Texte A, en justifiant votre évaluation. Soyez concis et précis dans votre analyse.
Cette réflexion n'apparaitra pas dans votre réponse finale, mais elle aurait pu se présenter de la forme suivante :

Justification :
- [Justification 1]
- [Justification 2]
- [Justification 3]
- ...

Ne donne que la note de complétude et rien d'autre !
""".strip()

_config = {
    "model": "gpt-4o",
    # "system_prompt": "Tu donnes...."
    "sampling_params": {"temperature": 0.2},
}


@metric_registry.register(
    name="judge_completude",
    description="[0-100] score of the completude correspondance between output and output_true",
    metric_type="llm",
    require=["output", "output_true"],
)
def judge_completude_metric(output, output_true, **kwargs):
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
