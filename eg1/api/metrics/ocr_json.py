import json
from rapidfuzz import fuzz as stringfuzz

from eg1.clients import LlmClient, split_think_answer
from eg1.utils import render_jinja, extract_code

from . import metric_registry

_template = """
You are tasked with generating a JSON representation from the analysis (OCR) of a given image.
Your goal is to create a JSON object that has the content of the image extracted in a structured format.

The JSON should be structured to represent the content of the image in a way that corresponds to standard markdown primitives. Here's how to approach this task:

The JSON should contain a list of blocks, where each block represents a distinct element in the image, such as headers, paragraphs, or tables.
Here is a an exemple of the json schema wanted:

```json
[
 {
   "type": "string (e.g Text, Table, Code, SectionHeader, Figure, Equation, Handwriting, PageFooter, PageHeader, Picture, TableOfContents etc)",
   "content": "string (mardown formated text)"
 },
 ...
]
```

Follow these guidelines when creating the JSON:

1. The main structure should be a list of blocks. Each block are object containing a `type` and a `text field`.
2. Each block is an object containing a `type` and a `text field`. They should correspond to a standard markdown primitive (e.g., Header, Paragraph, Table).
3. Identify headers based on font size, weight, or positioning. These should be represented as "Header" blocks.
4. Group continuous lines of text into "Paragraph" blocks.
5. Identify tabular data and represent it as "Table" blocks. Only create table blocks for actual tabular data, not for text formatting.
6. Do not create separate blocks for inline formatting (bold, italic) or URLs. Keep these within the relevant "Paragraph" block.
7. If you encounter lists, represent them as "List" blocks, with nested items if applicable.
8. For images or diagrams, use an "Image" block and include any available descriptive text.

Remember, the goal is to create a structured representation of the image content that could be easily converted to markdown or used for further processing. Focus on the main structural elements and avoid over-complicating the JSON with minor formatting details.

Do not explain your answer. Just answer with the JSON result directly.
""".strip()

_config = {}


@metric_registry.register(
    name="ocr_v1",
    description="Levenshtein distance between the output and the ground-truth markdown.",
    metric_type="ocr",
    require=["output", "markdown_true"],
)
def ocr_json_precision_metric(output, output_true, **kwargs):
    output = extract_code(output)
    try:
        blocks = json.loads(output)
        # assume json is a list of "visual) blocks that, between other, contains the 'text' attribute.
        output = "\n\n".join((x.get("text") or "") for x in blocks)
    except:
        pass
    score = stringfuzz.ratio(output, output_true)
    score = float(score)
    return score, None
