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


def calculate_key_level_scores(expected_data, extracted_data):
    """
    Calculate similarity scores for each top-level key in the JSON structure.
    
    Args:
        expected_data: Ground truth data structure (dict)
        extracted_data: LLM extracted data structure (dict)
    
    Returns:
        dict: Dictionary mapping each key to its similarity score
    """
    if not isinstance(expected_data, dict) or not isinstance(extracted_data, dict):
        return {}
    
    key_scores = {}
    all_keys = set(expected_data.keys()) | set(extracted_data.keys())
    print(">>> ALL KEYS", all_keys)
    
    for key in all_keys:
        expected_value = expected_data.get(key)
        extracted_value = extracted_data.get(key)
        
        # Calculate diff for this specific key
        key_diff = DeepDiff(expected_value, extracted_value, ignore_order=True)
        
        # Calculate score for this key
        key_score = calculate_similarity_score(expected_value, extracted_value, key_diff)
        key_scores[key] = key_score
    
    return key_scores


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
    metric_type="ops",  # This is an ops metric - it does its own evaluation
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
        tuple: (score, observation, result, keys_scores) where:
            - score: Overall similarity score between extracted and expected output (0-1)
            - observation: Detailed comparison and extracted JSON
            - result: Raw API response
            - keys_scores: Dict mapping each top-level key to its similarity score
    """
    # For ops metrics, we get the original model
    model = kwargs.get("model")
    if model is None:
        print("DEBUG: model is None in llm_structured_output_metric")
        return None, "Model is None", None
    
    # Get json_schema from sampling_params (where it should be passed via response_format)
    json_schema = None
    
    # Primary location: sampling_params.response_format.json_schema
    if hasattr(model, "sampling_params") and model.sampling_params:
        response_format = model.sampling_params.get("response_format", {})
        if response_format and "json_schema" in response_format:
            # Extract the schema from the response_format structure
            json_schema_obj = response_format.get("json_schema", {})
            if isinstance(json_schema_obj, dict):
                json_schema = json_schema_obj.get("schema", json_schema_obj)
            print(f"DEBUG: Found json_schema in sampling_params.response_format")
    
    # Fallback: check if passed directly in kwargs
    if not json_schema and "json_schema" in kwargs:
        json_schema = kwargs["json_schema"]
        print(f"DEBUG: Found json_schema in kwargs")
    
    if not json_schema:
        print(f"DEBUG: No json_schema found!")
        print(f"DEBUG: model.extra_params = {getattr(model, 'extra_params', 'N/A')}")
        print(f"DEBUG: model.sampling_params = {getattr(model, 'sampling_params', 'N/A')}")
        # Use a default schema if none provided
        json_schema = {
            "type": "object",
            "properties": {
                "persons": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "locations": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "organizations": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["persons", "locations", "organizations"]
        }
        print("DEBUG: Using default json_schema")
    
    # Get the text to analyze from output (not query)
    text_to_analyze = output  # The output is the text we need to analyze
    query_text = kwargs.get("query", "")
    
    # Setup model parameters
    system_prompt = getattr(model, "system_prompt", None)
    sampling_params = _config.get("sampling_params", {}).copy()
    if hasattr(model, "sampling_params") and model.sampling_params:
        for k, v in model.sampling_params.items():
            if k != "response_format":  # We'll add our own response_format
                sampling_params[k] = v

    # Check if model supports response_format (OpenAI-style)
    model_name = getattr(model, "name", "unknown")
    supports_response_format = model_name not in ["albert-large", "albert-small", "albert-api"]
    
    # Create the extraction prompt
    import json
    schema_str = json.dumps(json_schema, indent=2)
    
    if supports_response_format:
        # Model supports response_format, keep prompt simple
        prompt_content = f"""Extract structured information from the following text according to the JSON schema.

Text to analyze:
{text_to_analyze}

Extract entities matching the schema and return as JSON."""
        
        # Add response_format to sampling_params
        sampling_params["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": "data_extraction",
                "schema": json_schema,
                "strict": True
            }
        }
    else:
        # Model doesn't support response_format, include schema in prompt
        prompt_content = f"""Extract structured information from the following text.

You MUST return your response as valid JSON matching this exact schema:
{schema_str}

Text to analyze:
{text_to_analyze}

Important: Return ONLY valid JSON that matches the schema above. Do not include any other text, explanation, or markdown formatting."""

    messages = [{"role": "user", "content": prompt_content}]
    if system_prompt:
        messages.insert(0, {"role": "system", "content": system_prompt})

    # Debug output
    print("\n\n>>>>> DEBUG INFO:")
    print(">>>>> json_schema:", json_schema is not None)
    print(">>>>> model name:", model_name)
    print(">>>>> supports_response_format:", supports_response_format)
    print(">>>>> sampling_params keys:", list(sampling_params.keys()))
    
    # Call the LLM
    aiclient = LlmClient(base_url=getattr(model, "base_url", None), api_key=getattr(model, "api_key", None))
    result = aiclient.generate(model=model_name, messages=messages, **sampling_params)

    observation = result.choices[0].message.content
    think, answer = split_think_answer(observation)

    # Parse the extracted JSON
    extracted_data = None
    try:
        extracted_data = json.loads(answer if answer else observation)
    except json.JSONDecodeError:
        # Try to find JSON in the response
        import re
        json_match = re.search(r'\{.*\}', answer if answer else observation, re.DOTALL)
        if json_match:
            try:
                extracted_data = json.loads(json_match.group())
            except:
                pass
    
    # Parse the expected output (ground truth)
    expected_data = None
    try:
        expected_data = json.loads(output_true)
    except json.JSONDecodeError:
        print(f"DEBUG: Failed to parse output_true as JSON: {output_true[:200]}...")
    
    # Calculate similarity scores
    score = 0.0
    observation_dict = {}
    
    if extracted_data is None:
        observation_dict = {
            "error": "Failed to extract valid JSON from LLM response",
            "llm_response": (answer if answer else observation)[:500]
        }
    elif expected_data is None:
        observation_dict = {
            "error": "Failed to parse expected output as JSON",
            "output_true": output_true[:500]
        }
    else:
        # Calculate similarity
        diff = DeepDiff(expected_data, extracted_data, ignore_order=True)
        score = calculate_similarity_score(expected_data, extracted_data, diff)
        keys_scores = calculate_key_level_scores(expected_data, extracted_data)
        
        observation_dict = {
            "score": score,
            "extracted_data": extracted_data,
            "expected_data": expected_data,
            "key_scores": keys_scores,
            "differences": describe_diff(diff) if diff else "Perfect match"
        }
    
    print(f">>><<< extracted_data: {extracted_data}")
    print(f">>><<< expected_data: {expected_data}")
    print(f">>><<< score: {score}")
    
    # Convert observation dict to JSON string for storage
    observation = json.dumps(observation_dict, indent=2)
    
    return score, observation, result