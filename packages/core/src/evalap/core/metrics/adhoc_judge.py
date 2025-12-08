from evalap.clients import LlmClient, split_think_answer
from evalap.core.utils import render_jinja

from . import metric_registry

_config = {
    # "system_prompt": "Tu donnes...."
    "sampling_params": {"temperature": 0.2},
}


@metric_registry.register(
    name="judge_adhoc",
    description="A custom judge. The prompt params is use by the judge to evaluate the input.",
    metric_type="llm",
    require=[],  # @DEBUG: the require field should be generated dynamically from the prompt...
)
def judge_adhoc_metric(output, output_true, prompt: str, **kwargs):
    model = kwargs["model"]
    system_prompt = model.system_prompt or _config.get("system_prompt")
    sampling_params = _config.get("sampling_params", {}) | (model.sampling_params or {})
    messages = [
        {
            "role": "user",
            "content": render_jinja(prompt, output=output, output_true=output_true, **kwargs),
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
