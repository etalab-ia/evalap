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


Indique si la réponse C de l'agent correspond bien à la vrai réponse B ? En d'autres termes, la réponse de l'agent est-elle similaire à la bonne réponse?
Réponds 1 si oui ou 0 si non.
Ne retourne que 1 ou 0, rien d'autre !
""".strip()

_config = {
    "model": "gpt-4o",
    # "system_prompt": "Tu donnes...."
    "sampling_params": {"temperature": 0.2},
}


@metric_registry.register(
    name="judge_exactness",
    description="Binary similarity between output and output_true",
    metric_type="llm",
    require=["output", "output_true", "query"],
)
def judge_exactness_metric(output, output_true, query, **kwargs):
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
