from api.clients import LlmClient
from api.utils import render_jinja

from . import metric_registry

_template = """
Vous êtes un assistant IA chargé d'évaluer et de comparer deux textes pour déterminer si le Texte B est plus ou moins similaire (au sens de l'intention) au Texte A, sachant que A est la vérité terrain et B une réponse donnée par un autre LLM.

Texte A (vérité terrain) : {{output_true}}

Texte B (réponse d'un autre LLM) :  {{output}}

vous devez fournir une note de complétude indiquant le taux d'intersection entre B et A.
Cette note entre 0 et 100 apparaitera sous la forme (ne surtout pas afficher le %):
 XX

 Evidemment pour arriver à ce résultat final vous devez réfléchir à si le Texte B est plus ou moins similaire au Texte A, en justifiant votre évaluation. Soyez concis et précis dans votre analyse.
Cette réflexion n'apparaitra pas dans votre réponse finale, mais elle aurait pu se présenter de la forme suivante :

Justification :
- [Justification 1]
- [Justification 2]
- [Justification 3]
- ...

Ne donnez que la note de complétude et rien d'autre (sans le %)!
""".strip()

_config = {"model": "gpt-4o", "sampling_params": {"temperature": 0.2}}


@metric_registry.register(
    name="judge_completude", metric_type="llm", require=["output", "output_true"]
)
def judge_completude_metric(output, output_true, **kwargs):
    messages = [
        {"role": "user", "content": render_jinja(_template, output=output, output_true=output_true)}
    ]
    aiclient = LlmClient()
    result = aiclient.generate(model=_config["model"], messages=messages, **_config["sampling_params"])
    answer = result.choices[0].message.content
    score = answer.strip(" \n\"'.%")
    return score
