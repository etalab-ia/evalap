---
sidebar_position: 4
---

# Use Your Own Custom LLM-as-a-Judge Prompt

This guide explains how to use custom prompts for LLM-as-a-judge evaluation in EvalAP using parametrized metrics.

## Understanding Parametrized Metrics

EvalAP supports two types of metrics when designing an experiment:

1. **Non-parametrized metrics** (string): Simple metric names like `"judge_precision"` or `"generation_time"`
2. **Parametrized metrics** (dict): Metrics that accept custom parameters for fine-grained control

Parametrized metrics allow you to customize metric behavior by passing additional configuration options. This is particularly useful when you want to use your own evaluation prompts instead of the default ones.

## Parametrized Metric Structure

A parametrized metric is defined as a dictionary with three fields:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | The identifier of the metric to use |
| `aliased_name` | string | A custom display name shown in the frontend |
| `params` | object | An object containing the metric's required and optional parameters |

## Using Custom Judge Prompts with `judge_adhoc`

The `judge_adhoc` metric enables you to define your own LLM-as-a-judge evaluation criteria using a custom prompt.

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | string | Your custom evaluation prompt for the judge model |

### Example: Simple Custom Judge

Here's how to create an experiment with a custom judge prompt:

```python
import os
import requests

API_URL = "http://localhost:8000/v1"
EVALAP_API_KEY = os.getenv("EVALAP_API_KEY")

# Replace with your API key or authentication token (or None if launch locally)
HEADERS = {
    "Authorization": "Bearer EVALAP_API_KEY",
    "Content-Type": "application/json"
}

# Define a custom judge prompt
custom_prompt = """Evaluate if the answer is polite and professional.
Return 1 if the answer meets both criteria, 0 otherwise.

Query: {{query}}
Answer: {{output}}
"""

# Design the experiment with a parametrized metric
experiment = {
    "name": "politeness_evaluation",
    "dataset": "my_dataset",
    "model": {
        "name": "gpt-4.1",
        "base_url": "https://api.openai.com/v1",
        "api_key": os.getenv("OPENAI_API_KEY")
    },
    "metrics": [
        # Non-parametrized metric (string)
        "generation_time",
        # Parametrized metric (dict)
        {
            "name": "judge_adhoc",
            "aliased_name": "Politeness Score",
            "params": {
                "prompt": custom_prompt
            }
        }
    ]
}

# Run the experiment
response = requests.post(f'{API_URL}/experiment', json=experiment, headers=HEADERS)
experiment_id = response.json()["id"]
print(f"Experiment {experiment_id} is running")
```

### Example: Multiple Custom Judges

You can use multiple parametrized metrics in the same experiment, each with different custom prompts:

```python
# Define multiple custom judge prompts
accuracy_prompt = """Evaluate if the answer correctly addresses the query.
Return 1 if accurate, 0 otherwise.

Query: {{query}}
Answer: {{output}}
Expected: {{output_true}}
"""

clarity_prompt = """Evaluate if the answer is clear and easy to understand.
Return 1 if clear, 0 otherwise.

Answer: {{output}}
"""

experiment = {
    "name": "multi_criteria_evaluation",
    "dataset": "my_dataset",
    "model": {"name": "gpt-4o", "base_url": "https://api.openai.com/v1", "api_key": os.getenv("OPENAI_API_KEY")},
    "metrics": [
        {
            "name": "judge_adhoc",
            "aliased_name": "Accuracy",
            "params": {"prompt": accuracy_prompt}
        },
        {
            "name": "judge_adhoc",
            "aliased_name": "Clarity",
            "params": {"prompt": clarity_prompt}
        },
        "generation_time"
    ]
}
```

## Available Variables in Custom Prompts

Your custom prompt can reference dataset columns and model outputs using template variables. Common variables include (there must present in the dataset or auto-generated, like query and contexts if the model is supported by EvalAP):

- `{{query}}`: The input query from your dataset
- `{{output}}`: The model's generated answer
- `{{output_true}}`: The ground truth answer (if available in your dataset)
- `{{context}}`: Additional context provided to the model
- `{{retrieval_context}}`: Retrieved information used in generation

Ensure that any variables you reference in your prompt correspond to columns in your dataset or fields generated during evaluation.

:::tip Judge Model Configuration
By default, custom judge prompts use EvalAP's configured judge model. You can specify a different judge model using the `judge_model` parameter at the experiment level, as described in the [Create a Simple Experiment](./create-a-simple-experiment#configuring-a-llm-as-a-judge-model) guide.
:::

## Mixing Parametrized and Non-Parametrized Metrics

You can freely mix both types of metrics in your experiment:

```python
experiment = {
    "name": "mixed_metrics_experiment",
    "dataset": "my_dataset",
    "model": {"name": "gpt-4o", "base_url": "https://api.openai.com/v1", "api_key": os.getenv("OPENAI_API_KEY")},
    "metrics": [
        # Standard metrics (non-parametrized)
        "generation_time",
        "output_length",
        "judge_precision",
        # Custom judge metric (parametrized)
        {
            "name": "judge_adhoc",
            "aliased_name": "Custom Evaluation",
            "params": {
                "prompt": "Your custom prompt here..."
            }
        }
    ]
}
```

:::info
The `aliased_name` field is especially useful when using multiple instances of the same metric with different parameters, as it helps distinguish them in the frontend results view.
:::
