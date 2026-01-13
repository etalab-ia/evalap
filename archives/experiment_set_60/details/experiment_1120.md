# Experiment 1120

[← Back to Index](../index.md)

**Name:** albert_OCR_v2__0

**Readme:** None

**Dataset:** OCR_marker_benchmark

**Judge model:** None

**Model:** {'name': 'mistralai/Mistral-Small-3.1-24B-Instruct-2503', 'base_url': 'https://albert.api.etalab.gouv.fr/v1', 'aliased_name': None, 'system_prompt': 'You are tasked with generating a JSON representation from the analysis (OCR) of a given image. \nYour goal is to create a JSON object that has the content of the image extracted in a structured format. \n\nThe JSON should be structured to represent the content of the image in a way that corresponds to standard markdown primitives. Here\'s how to approach this task:\n\nThe JSON should contain a list of blocks, where each block represents a distinct element in the image, such as headers, paragraphs, or tables.\nHere is a an exemple of the json schema wanted: \n\nSchema:\n```json\n[\n {\n   "type": "string (e.g  Text, Table, Code, SectionHeader, Figure, Equation, Handwriting, PageFooter, PageHeader, Picture, TableOfContents etc)",\n   "text": "string (mardown formated text)"\n },\n ...\n]\n```\n\nExample:\n```json\n[\n {\n    "type": "Header", "text": "## I am a level 2 header"\n },\n {\n   "type": "Paragraph", "text": "I am a **paragraph**"\n }\n]\n````\n\nFollow these guidelines when creating the JSON:\n\n1. The main structure should be a list of blocks. Each block are object containing a `type` and a `text field`.\n2. Each block is an object containing a `type` and a `text field`. They should correspond to a standard markdown primitive (e.g., Header, Paragraph, Table).\n3. Identify headers based on font size, weight, or positioning. These should be represented as "Header" blocks.\n4. Group continuous lines of text into "Paragraph" blocks.\n5. Identify tabular data and represent it as "Table" blocks. Only create table blocks for actual tabular data, not for text formatting.\n6. Do not create separate blocks for inline formatting (bold, italic) or URLs. Keep these within the relevant "Paragraph" block.\n7. If you encounter lists, represent them as "List" blocks, with nested items if applicable.\n8. For images or diagrams, use an "Image" block and include any available descriptive text.\n\nRemember, the goal is to create a structured representation of the image content that could be easily converted to markdown or used for further processing. Focus on the main structural elements and avoid over-complicating the JSON with minor formatting details.\n\nDo not explain your answer. Just answer with the JSON result directly.\n', 'prelude_prompt': None, 'sampling_params': {'temperature': 0.2}, 'extra_params': None, 'id': 1076, 'has_raw_output': False}

## Data Table

| answer   | answer_error_msg   | result_output_length   | result_generation_time   | result_ocr_v1   |
|----------|--------------------|------------------------|--------------------------|-----------------|
