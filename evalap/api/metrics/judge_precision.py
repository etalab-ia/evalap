from evalap.clients import LlmClient, split_think_answer
from evalap.utils import render_jinja

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
    # "system_prompt": "Tu donnes...."
    "sampling_params": {"temperature": 0.2},
}


@metric_registry.register(
    name="judge_precision",
    description="[0;1] The 'judge_precision' metric indicates whether the expected response is contained in the alternative response given. It returns 1 if yes, otherwise 0. It is used to verify that the expected key information is present in the response provided, thus ensuring an accurate and complete response.",
    metric_type="llm",
    require=["output", "output_true", "query"],
)
def judge_precision_metric(output, output_true, **kwargs):
    model = kwargs["model"]
    system_prompt =  model.system_prompt or _config.get("system_prompt")
    sampling_params = _config.get("sampling_params", {}) | (model.sampling_params or {})
    messages = [
        {
            "role": "user",
            "content": render_jinja(_template, output=output, output_true=output_true, **kwargs),
        }
    ]
    if system_prompt:
        messages = [{"role": "system", "content": system_prompt}] + messages
    aiclient = LlmClient(base_url=model.base_url, api_key=model.api_key)
    result = aiclient.generate(model=model.name, messages=messages, **sampling_params)
    observation = result.choices[0].message.content
    think, answer = split_think_answer(observation)
    score = answer.strip(" \n\"'.%")
    try:
        score = float(score)
    except ValueError:
        score = None
    return score, observation, result
