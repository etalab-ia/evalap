import json
from rapidfuzz import fuzz as stringfuzz

from eg1.clients import LlmClient, split_think_answer
from eg1.utils import render_jinja, extract_code

from . import metric_registry

_config = {}


@metric_registry.register(
    name="ocr_v1",
    description="Levenshtein distance between the output and the ground-truth markdown.",
    metric_type="ocr",
    require=["output", "output_true"],
)
def ocr_json_precision_metric(output, output_true, **kwargs):
    output = extract_code(output)
    try:
        # Assume that ocr metrics can receive a json list of block containing a "text" (markdown) field
        blocks = json.loads(output)
        # assume json is a list of "visual) blocks that, between other, contains the 'text' attribute.
        output = "\n\n".join((x.get("text") or "") for x in blocks)
    except:
        pass
    score = stringfuzz.ratio(output, output_true)
    score = float(score)
    return score, None
