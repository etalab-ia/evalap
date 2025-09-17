from evalap.clients import LlmClient, split_think_answer
from evalap.utils import render_jinja

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
    description="La métrique 'judge_exactness' indique simplement si la réponse générée par un agent correspond exactement à la bonne réponse attendue. Elle retourne 1 si la réponse est bien similaire à la vérité terrain, sinon 0. Cette métrique sert à valider la correspondance précise dans des cas où la fidélité stricte à la bonne réponse est essentielle.",
    metric_type="llm",
    require=["output", "output_true", "query"],
)
def judge_exactness_metric(output, output_true, **kwargs):
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
