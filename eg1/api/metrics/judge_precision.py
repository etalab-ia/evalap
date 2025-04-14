from eg1.clients import LlmClient, split_think_answer
from eg1.utils import render_jinja

from . import metric_registry

_template = """
Etant donnée la question A suivante :

<A>
{{query}}
</A>


Et étant donnée la réponse attendue B suivante :

<B>
{{output_true}}
</B>

Et étant donnée la réponse C alternative à évaluer, suivante :

<C>
{{output}}
</C>


Indique si la réponse attendue B est contenue dans la réponse C.
Réponds 1 si oui ou 0 si non.

Ne retourne que 1 ou 0, rien d'autre !
""".strip()

_config = {
    "model": "gpt-4o",
    # "system_prompt": "Tu donnes...."
    "sampling_params": {"temperature": 0.2},
}


@metric_registry.register(
    name="judge_precision",
    description="Binary precision of the output_true. Equal to one if the correct answer is contained in the given answer.",
    metric_type="llm",
    require=["output", "output_true", "query"],
)
def judge_precision_metric(output, output_true, **kwargs):
    config = _config | {k: v for k, v in kwargs.items() if k in _config}
    messages = [
        {
            "role": "user",
            "content": render_jinja(_template, output=output, output_true=output_true, **kwargs),
        }
    ]
    aiclient = LlmClient()
    result = aiclient.generate(model=config["model"], messages=messages, **config["sampling_params"])
    observation = result.choices[0].message.content
    think, answer = split_think_answer(observation)
    score = answer.strip(" \n\"'.%")
    try:
        score = float(score)
    except ValueError:
        score = None
    return score, observation
