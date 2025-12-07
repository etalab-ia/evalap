---
sidebar_position: 1
---

# Adding a New Metric

This guide will walk you through the process of adding a custom evaluation metric to Evalap.

## Understanding Metrics in Evalap

Evalap uses a metric registry system where metrics are registered using decorators. There are three types of metrics:

- **LLM-as-judge metrics**: Use language models to evaluate outputs
- **DeepEval metrics**: Integrate with the DeepEval library
- **Human metrics**: For human-in-the-loop evaluation

Each metric specifies its required inputs and returns a score along with an explanation.

## Prerequisites

Before adding a new metric, ensure you have:

- A local development environment set up
- Understanding of the metric you want to implement
- Basic knowledge of Python and decorators

## Example 1: Creating an LLM-as-Judge Metric

This example shows how to create a metric that uses an LLM to evaluate outputs. Create a new Python file in the `evalap/api/metrics/` directory:

```python
# evalap/api/metrics/my_custom_metric.py

from evalap.clients import LlmClient, split_think_answer
from evalap.utils import render_jinja

from . import metric_registry

# Define your prompt template for the LLM-as-judge metric
_template = """
Given the following question:

<question>
{{query}}
</question>

And the expected answer:

<expected>
{{output_true}}
</expected>

And the actual answer to evaluate:

<actual>
{{output}}
</actual>

Evaluate how well the actual answer matches the expected answer.
Score from 0 to 1, where 1 is a perfect match.

Return only the numeric score!
""".strip()

# Configuration for LLM-as-judge metrics
_config = {
    "model": "gpt-4o",
    "sampling_params": {"temperature": 0.2},
}

@metric_registry.register(
    name="my_custom_metric",
    description="Evaluates how well the output matches the expected answer",
    metric_type="llm",  # or "deepeval" or "human"
    require=["output", "output_true", "query"],  # Required inputs
)
def my_custom_metric(output, output_true, **kwargs):
    """
    Compute the custom metric score.

    Args:
        output: The model's output to evaluate
        output_true: The expected/reference output
        **kwargs: Additional parameters (e.g., query, context)

    Returns:
        tuple: (score, observation) where score is numeric and observation is explanation
    """
    # For LLM-as-judge metrics
    config = _config | {k: v for k, v in kwargs.items() if k in _config}

    messages = [
        {
            "role": "user",
            "content": render_jinja(_template, output=output, output_true=output_true, **kwargs),
        }
    ]

    aiclient = LlmClient()
    result = aiclient.generate(
        model=config["model"],
        messages=messages,
        **config["sampling_params"]
    )

    observation = result.choices[0].message.content
    think, answer = split_think_answer(observation)

    # Parse the score
    score = answer.strip(" \n\"'.%")
    try:
        score = float(score)
    except ValueError:
        score = None

    return score, observation
```

## Example 2: Creating a Non-LLM Metric

This example demonstrates how to create a simple metric that doesn't use an LLM for evaluation. These metrics use deterministic logic or mathematical calculations:

```python
# evalap/api/metrics/exact_match.py

from . import metric_registry

@metric_registry.register(
    name="exact_match",
    description="Binary metric that checks if output exactly matches expected",
    metric_type="llm",  # Even simple metrics can be marked as "llm" type
    require=["output", "output_true"],
)
def exact_match_metric(output, output_true, **kwargs):
    """Check if output exactly matches expected output."""
    # Normalize strings for comparison
    output_normalized = output.strip().lower()
    expected_normalized = output_true.strip().lower()

    # Calculate score
    score = 1.0 if output_normalized == expected_normalized else 0.0

    # Provide explanation
    if score == 1.0:
        observation = "Exact match found"
    else:
        observation = f"No match: expected '{output_true}' but got '{output}'"

    return score, observation
```

## Understanding Required Inputs

The `require` parameter specifies which inputs your metric needs. Common options include:

- `output`: The model's generated answer
- `output_true`: The expected/reference answer
- `query`: The input question/prompt
- `context`: Additional context provided
- `retrieval_context`: Retrieved documents (for RAG metrics)
- `reasoning`: Chain-of-thought reasoning

## Metric Registration

The metric is automatically registered when the file is placed in the `evalap/api/metrics/` directory. The registration happens through the `__init__.py` file which imports all Python files in the directory.

## Testing Your Metric

Create tests for your metric:

```python
# tests/api/metrics/test_my_custom_metric.py

import pytest
from evalap.api.metrics import metric_registry

def test_my_custom_metric():
    metric_func = metric_registry.get_metric_function("my_custom_metric")

    # Test perfect match
    score, observation = metric_func(
        output="Paris is the capital of France",
        output_true="Paris is the capital of France",
        query="What is the capital of France?"
    )
    assert score == 1.0

    # Test partial match
    score, observation = metric_func(
        output="Paris",
        output_true="Paris is the capital of France",
        query="What is the capital of France?"
    )
    assert 0 < score < 1

    # Test no match
    score, observation = metric_func(
        output="London is the capital of UK",
        output_true="Paris is the capital of France",
        query="What is the capital of France?"
    )
    assert score == 0.0
```

## Using Your Metric

Once registered, your metric can be used in experiments:

```python
from evalap.api.metrics import metric_registry

# Get the metric function
metric_func = metric_registry.get_metric_function("my_custom_metric")

# Use it to evaluate
score, reason = metric_func(
    output="The model's answer",
    output_true="The expected answer",
    query="What is the question?"
)

print(f"Score: {score}")
print(f"Reason: {reason}")
```

## Advanced Topics

### Integrating DeepEval Metrics

Evalap automatically integrates several DeepEval metrics. To add a new DeepEval metric:

1. Add the metric class name to the `classes` list in `evalap/api/metrics/__init__.py`
2. The system will automatically register it with appropriate naming and requirements

### Handling Different Input Types

For metrics that require different inputs than the standard ones, you can map them using the `deepeval_require_map`:

```python
deepeval_require_map = {
    "input": "query",
    "actual_output": "output",
    "expected_output": "output_true",
    "context": "context",
    "retrieval_context": "retrieval_context",
    "reasoning": "reasoning",
}
```

### Error Handling

Always handle potential errors gracefully:

```python
try:
    score = float(answer)
except ValueError:
    score = None
    observation = "Failed to parse score from LLM response"
```

## Best Practices

1. **Clear Naming**: Use descriptive names that indicate what the metric measures
2. **Documentation**: Provide clear descriptions in the `description` parameter
3. **Consistent Scoring**: Use a consistent scale (typically 0-1)
4. **Explanations**: Always return meaningful observations/reasons with scores
5. **Input Validation**: Validate required inputs before processing
6. **Temperature Settings**: For LLM-as-judge metrics, use low temperature for consistency

## Conclusion

By following these steps, you can add custom metrics to Evalap that integrate seamlessly with the evaluation platform. The metric registry system makes it easy to add new evaluation criteria while maintaining consistency across the platform.
