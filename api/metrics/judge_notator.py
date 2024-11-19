from api.clients import LlmClient
from api.utils import render_jinja

from . import metric_registry

_template = """
Etant donnée la question A suivante :

<A>
{{query}}
</A>


Et étant donnée la bonne réponse B associée :

<B>
{{output_true}}
</B>


Et étant donnée la réponse C générée par un autre agent, à évaluer :

<C>
{{output}}
</C>


Tu vas évaluer la similarité sémantique entre la réponse de référence B et la réponse à évaluer C, en attribuant une note comprise entre 1 et 10.

Directives pour la notation :
- 10 : Les réponses sont sémantiquement identiques ou presque, même si les mots utilisés sont différents.
- 7-9 : Les réponses sont très similaires sur le plan du sens, avec seulement des différences mineures ou des détails supplémentaires dans l'une des réponses.
- 4-6 : Les réponses partagent des éléments de sens communs, mais il y a des différences notables ou des omissions importantes.
- 1-3 : Les réponses sont significativement différentes sur le plan du sens ou la réponse à évaluer ne répond pas correctement à la question.

Points importants à considérer :
1. Concentre-toi sur le sens global et l'information principale véhiculée par chaque réponse.
2. Ne pénalise pas les différences de formulation tant que le sens reste le même.
3. Les synonymes, paraphrases, ou reformulations qui conservent le sens original doivent être considérés comme équivalents.
4. Une réponse plus courte mais qui capture l'essentiel de l'information peut obtenir une note élevée si elle est sémantiquement équivalente.

Ne retourne que la note, rien d'autre !
""".strip()

_config = {
    "model": "gpt-4o",
    # "system_prompt": "Tu donnes...."
    "sampling_params": {"temperature": 0.2},
}


@metric_registry.register(
    name="judge_notator",
    description="[1-10] score semantic similarity between output and output_true",
    metric_type="llm",
    require=["output", "output_true", "query"],
)
def judge_notator_metric(output, output_true, query, **kwargs):
    messages = [
        {
            "role": "user",
            "content": render_jinja(_template, output=output, output_true=output_true, query=query, **kwargs),
            }
    ]
    aiclient = LlmClient()
    result = aiclient.generate(
        model=_config["model"], messages=messages, **_config["sampling_params"]
    )
    answer = result.choices[0].message.content
    score = answer.strip(" \n\"'.%")
    try:
        score = float(score)
    except ValueError:
        score = None
    return score, answer
