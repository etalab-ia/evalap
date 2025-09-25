import json
from evalap.clients import LlmClient, split_think_answer
from evalap.utils import render_jinja
from deepdiff import DeepDiff


from . import metric_registry


_config = {
    "sampling_params": {"temperature": 0.1},  # Low temperature for consistent structured output
}


def count_total_values(data):
    """
    Recursively count all values in a nested data structure.
    This includes:
    - All leaf values (strings, numbers, booleans, None)
    - Each item in arrays/lists
    - Each key-value pair in objects/dictionaries
    """
    if data is None:
        return 1
    elif isinstance(data, (str, int, float, bool)):
        return 1
    elif isinstance(data, list):
        return sum(count_total_values(item) for item in data)
    elif isinstance(data, dict):
        return sum(count_total_values(value) for value in data.values())
    else:
        return 1  # For any other type


def calculate_similarity_score(expected_data, extracted_data, diff):
    """
    Calculate similarity score based on total number of values rather than just keys.
    
    Args:
        expected_data: Ground truth data structure
        extracted_data: LLM extracted data structure  
        diff: DeepDiff result between expected and extracted data
    
    Returns:
        float: Score between 0 and 1, where 1 is perfect match
    """
    if expected_data is None and extracted_data is None:
        return 1.0
    if expected_data is None or extracted_data is None:
        return 0.0
    
    if not diff:
        return 1.0
    
    # Count total values in expected data
    total_expected_values = count_total_values(expected_data)
    
    # Count the number of differences
    diff_count = 0
    
    # Count value changes
    diff_count += len(diff.get('values_changed', {}))
    
    # Count type changes
    diff_count += len(diff.get('type_changes', {}))
    
    # Count missing items (in expected but not in extracted)
    for removed_items in diff.get('dictionary_item_removed', {}).values():
        diff_count += count_total_values(removed_items)
    for removed_items in diff.get('iterable_item_removed', {}).values():
        diff_count += count_total_values(removed_items)
    
    # Count extra items (in extracted but not in expected)  
    for added_items in diff.get('dictionary_item_added', {}).values():
        diff_count += count_total_values(added_items)
    for added_items in diff.get('iterable_item_added', {}).values():
        diff_count += count_total_values(added_items)
    
    # Calculate score
    if total_expected_values == 0:
        return 1.0 if diff_count == 0 else 0.0
    
    score = max(0.0, 1.0 - (diff_count / total_expected_values))
    return score


def describe_diff(diff):
    """
    Compare LLM extracted data to ground truth and return a human-readable report:
    - Present in ground truth but missing in LLM output
    - Present in LLM output but not in ground truth
    - Present in both but different values
    """
    if not diff:
        return "Perfect match! The LLM output exactly matches the ground truth."

    descriptions = []

    # Values that changed
    for path, change in diff.get('values_changed', {}).items():
        descriptions.append(
            f"- At {path}, value differs: ground truth has '{change['old_value']}', LLM output has '{change['new_value']}'"
        )

    # Type changes
    for path, change in diff.get('type_changes', {}).items():
        descriptions.append(
            f"- At {path}, type differs: ground truth is {change['old_type']} ('{change['old_value']}'), LLM output is {change['new_type']} ('{change['new_value']}')"
        )

    # Missing items in LLM output
    for path, value in diff.get('dictionary_item_removed', {}).items():
        descriptions.append(f"- Present in ground truth but missing in LLM output: {path} → {value}")
    for path, value in diff.get('iterable_item_removed', {}).items():
        descriptions.append(f"- Present in ground truth but missing in LLM output: {path} → {value}")

    # Extra items in LLM output
    for path, value in diff.get('dictionary_item_added', {}).items():
        descriptions.append(f"- Present in LLM output but not in ground truth: {path} → {value}")
    for path, value in diff.get('iterable_item_added', {}).items():
        descriptions.append(f"- Present in LLM output but not in ground truth: {path} → {value}")

    return "\n".join(descriptions)


@metric_registry.register(
    name="llm_structured_output",
    description="Extract structured content from raw text using LLM with JSON schema",
    metric_type="llm",  # Use 'ops' type since this metric does its own evaluation without needing a judge
    require=["output", "output_true", "query"],
)
def llm_structured_output_metric(output, output_true, **kwargs):
    """
    Extract structured content from raw text using LLM with JSON schema.

    Args:
        output: The raw text to extract structured information from
        output_true: The expected structured output (ground truth) as JSON string
        query: The query/context (may contain schema information)
        **kwargs: Additional parameters including:
            - json_schema: The JSON schema defining what to extract
            - model: The model configuration

    Returns:
        tuple: (score, observation, result) where:
            - score: Similarity score between extracted and expected output (0-1)
            - observation: Detailed comparison and extracted JSON
            - result: Raw API response
    """
    model = kwargs["model"]
    json_schema = kwargs.get("json_schema")
    query = kwargs["query"]
    system_prompt = model.get("system_prompt") or _config.get("system_prompt")
    sampling_params = _config.get("sampling_params", {}) | (model.get("sampling_params") or {})

    # Add JSON schema to sampling params for structured output
    sampling_params["response_format"] = {"type": "json_schema", "json_schema": json_schema}

    kwargs.pop("json_schema", None)  # remove if exists

    messages = [
        {
            "role": "user",
            "content": query,
        }
    ]

    if system_prompt:
        messages = [{"role": "system", "content": system_prompt}] + messages

    aiclient = LlmClient(base_url=model.get("base_url"), api_key=model.get("api_key"))
    result = aiclient.generate(model=model.get("name"), messages=messages, **sampling_params)

    observation = result.choices[0].message.content
    think, answer = split_think_answer(observation)

    # Parse the extracted JSON
    try:
        extracted_data = json.loads(answer)
    except json.JSONDecodeError:
        extracted_data = None
        observation = f"Failed to parse extracted JSON: {answer}"

    # Parse the expected output (ground truth)
    try:
        expected_data = json.loads(output_true)
    except json.JSONDecodeError:
        expected_data = None
        observation = f"Failed to parse expected JSON: {output_true}"

    # Calculate similarity score and get diff (computed only once)
    score = None
    diff = None
    if extracted_data is not None and expected_data is not None:
        diff = DeepDiff(expected_data, extracted_data, ignore_order=True)
        score = calculate_similarity_score(expected_data, extracted_data, diff)

    # Create detailed observation
    if score is not None and diff is not None:
        total_values_expected_data = count_total_values(expected_data)
        total_values_extracted_data = count_total_values(extracted_data)
        observation = f"Total values extracted in ground truth : {total_values_expected_data}\n"
        observation += f"Total values extracted in llm output   : {total_values_extracted_data}\n"
        observation += f"Similarity score: {score:.3f}\n\n"
        observation += describe_diff(diff)

    return score, observation, result