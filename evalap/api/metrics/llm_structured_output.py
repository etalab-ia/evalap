import json
import re
from evalap.clients import LlmClient, split_think_answer
from deepdiff import DeepDiff
from . import metric_registry


def parse_json_from_response(response: str) -> dict | None:
    """
    Extract and parse JSON from an LLM response.
    Handles responses that may contain extra text or markdown formatting.
    """
    # Try to parse the response directly
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        pass
    
    # Try to find JSON in the response using regex
    # Look for content between curly braces
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    
    # Try to find JSON in markdown code blocks
    code_block_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
    if code_block_match:
        try:
            return json.loads(code_block_match.group(1))
        except json.JSONDecodeError:
            pass
    
    return None


def calculate_similarity_score(expected_data: dict, extracted_data: dict) -> tuple[float, dict]:
    """
    Calculate similarity score between expected and extracted JSON data.
    
    Returns:
        tuple: (overall_score, detailed_scores)
    """
    if not expected_data or not extracted_data:
        return 0.0, {}
    
    # Use DeepDiff to find differences
    diff = DeepDiff(expected_data, extracted_data, ignore_order=True)
    
    if not diff:
        return 1.0, {"status": "perfect_match"}
    
    # Calculate scores for each field
    field_scores = {}
    total_score = 0
    field_count = 0
    
    # Get all fields from both dictionaries
    all_fields = set(expected_data.keys()) | set(extracted_data.keys())
    
    for field in all_fields:
        field_count += 1
        expected_value = expected_data.get(field, [])
        extracted_value = extracted_data.get(field, [])
        
        # Calculate field-specific score
        if field not in expected_data:
            # Extra field in extracted
            field_scores[field] = {"score": 0, "reason": "unexpected_field"}
        elif field not in extracted_data:
            # Missing field in extracted
            field_scores[field] = {"score": 0, "reason": "missing_field"}
        elif isinstance(expected_value, list) and isinstance(extracted_value, list):
            # Compare lists
            expected_set = set(expected_value)
            extracted_set = set(extracted_value)
            
            if expected_set == extracted_set:
                field_scores[field] = {"score": 1.0, "reason": "exact_match"}
                total_score += 1.0
            else:
                # Calculate Jaccard similarity
                intersection = expected_set & extracted_set
                union = expected_set | extracted_set
                if union:
                    jaccard_score = len(intersection) / len(union)
                    field_scores[field] = {
                        "score": jaccard_score,
                        "missing": list(expected_set - extracted_set),
                        "extra": list(extracted_set - expected_set),
                        "correct": list(intersection)
                    }
                    total_score += jaccard_score
                else:
                    field_scores[field] = {"score": 1.0, "reason": "both_empty"}
                    total_score += 1.0
        else:
            # Direct comparison for non-list fields
            if expected_value == extracted_value:
                field_scores[field] = {"score": 1.0, "reason": "exact_match"}
                total_score += 1.0
            else:
                field_scores[field] = {
                    "score": 0,
                    "expected": expected_value,
                    "got": extracted_value
                }
    
    overall_score = total_score / field_count if field_count > 0 else 0
    
    return overall_score, field_scores


@metric_registry.register(
    name="llm_structured_output",
    description="Extract structured content from raw text using LLM and compare with ground truth",
    metric_type="llm",  # Mark as LLM type since it uses LLM for extraction
    require=["output", "output_true", "query"],
)
def llm_structured_output_metric(output, output_true, **kwargs):
    """
    Extract structured content from raw text using LLM and compare with ground truth.
    
    This metric:
    1. Takes raw text from 'output' parameter
    2. Uses judge_model (with its prompts and parameters) to extract structured data
    3. Compares extracted JSON with ground truth JSON
    4. Returns similarity scores
    
    Args:
        output: The raw text to extract structured information from
        output_true: The expected structured output (ground truth) as JSON string
        query: The original query/context (included for compatibility)
        **kwargs: Additional parameters including:
            - model: The judge_model configuration containing:
                - prelude_prompt: The extraction prompt template (with {text} placeholder)
                - system_prompt: Optional system prompt
                - sampling_params: Temperature and other generation parameters
    
    Returns:
        tuple: (score, observation, result) where:
            - score: Overall similarity score between extracted and expected (0-1)
            - observation: Detailed comparison results as JSON string
            - result: Raw LLM API response
    """
    # Get the judge model configuration
    print("KWARGS", kwargs)
    judge_model = kwargs.get("model")
    if not judge_model:
        return None, json.dumps({"error": "No judge model provided"}), None
    
    # Get the text to analyze from output parameter
    text_to_analyze = output
    
    # Build the extraction prompt
    # The prelude_prompt should contain the extraction instructions and JSON schema
    # It should have a {text} placeholder that we replace with the actual text
    extraction_prompt = getattr(judge_model, "prelude_prompt", None)
    system_prompt = getattr(judge_model, "system_prompt", None)
    
    if not extraction_prompt:
        # Fallback to a simple default prompt if none provided
        extraction_prompt = """Extract structured information from the following text and return as JSON.
Text: {text}

Return only valid JSON."""
    
    # Replace the {text} placeholder with the actual text
    prompt_content = extraction_prompt.replace("{text}", text_to_analyze)
    
    # Build messages for the LLM
    messages = [{"role": "user", "content": prompt_content}]
    if system_prompt:
        messages.insert(0, {"role": "system", "content": system_prompt})
    
    # Get sampling parameters from judge_model
    sampling_params = {}
    if hasattr(judge_model, "sampling_params") and judge_model.sampling_params:
        sampling_params = judge_model.sampling_params.copy()
    
    # Call the LLM to extract structured data
    try:
        aiclient = LlmClient(
            base_url=getattr(judge_model, "base_url", None),
            api_key=getattr(judge_model, "api_key", None)
        )
        
        result = aiclient.generate(
            model=getattr(judge_model, "name", "unknown"),
            messages=messages,
            **sampling_params
        )
        
        # Get the LLM response
        llm_response = result.choices[0].message.content
        think, answer = split_think_answer(llm_response)
        
    except Exception as e:
        error_msg = f"LLM extraction failed: {str(e)}"
        return 0.0, json.dumps({"error": error_msg}), None
    
    # Parse the extracted JSON from the LLM response
    extracted_data = parse_json_from_response(answer if answer else llm_response)
    
    # Parse the expected output (ground truth)
    try:
        expected_data = json.loads(output_true) if isinstance(output_true, str) else output_true
    except json.JSONDecodeError as e:
        return 0.0, json.dumps({
            "error": f"Failed to parse ground truth JSON: {str(e)}",
            "output_true": output_true[:500]
        }), result
    
    # Handle extraction failures
    if extracted_data is None:
        observation = {
            "score": 0.0,
            "error": "Failed to extract valid JSON from LLM response",
            "llm_response": (answer if answer else llm_response)[:500],
            "expected_data": expected_data
        }
        return 0.0, json.dumps(observation, indent=2), result
    
    # Calculate similarity scores
    overall_score, field_scores = calculate_similarity_score(expected_data, extracted_data)
    
    # Build detailed observation
    observation = {
        "score": overall_score,
        "extracted_data": extracted_data,
        "expected_data": expected_data,
        "field_scores": field_scores,
        "extraction_details": {
            "model": getattr(judge_model, "name", "unknown"),
            "temperature": sampling_params.get("temperature", "unknown"),
            "prompt_type": getattr(judge_model, "aliased_name", "unknown")
        }
    }
    
    # Add thinking process if available
    if think:
        observation["llm_thinking"] = think[:500]  # Truncate for storage
    
    return overall_score, json.dumps(observation, indent=2), result