---
sidebar_position: 3
---

# Create an Experiment Set

This guide explains how to create and run an experiment set evaluation  in EvalAP, which allows you to compare multiple models or configurations.

## Why Use Experiment Sets?

Meaningful evaluations rarely consist of a single experiment. To draw valid conclusions about model performance, you need:

1. **Comparative analysis**: Compare different models on the same dataset
2. **Reproducibility**: Run the same experiment multiple times to account for variability
3. **Parameter exploration**: Test how different configurations affect performance
4. **Comprehensive evaluation**: Assess models across multiple metrics

Experiment sets in EvalAP make it easy to organize related experiments and analyze their results collectively.

## Creating an Experiment Set via the API

There are two main ways to create an experiment set:

1. **Cross-validation (CV) schema**: Automatically generate experiments by combining parameters
2. **Manual definition**: Explicitly define each experiment in the set

### Using the Cross-Validation Schema

The CV schema is powerful for generating multiple experiments from a grid of parameters:

```python
import os
import requests

# Replace with your Evalap API endpoint
API_URL = "https://evalap.etalab.gouv.fr/v1"

# Replace with your API key or authentication token
HEADERS = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

# Define your experiment set with CV schema
expset_name = "model_comparison_v1"
expset_readme = "Comparing performance of various LLMs on a QA dataset."
metrics = ["judge_precision", "output_length", "generation_time"]

# Parameters common to all experiments
common_params = {
    "dataset": "qa_benchmark_v2",  # assuming this dataset has been added before
    "model": {"sampling_params": {"temperature": 0.2}},
    "metrics": metrics,
    "judge_model": "gpt-4o",
}

# Parameters that will vary across experiments
grid_params = {
    "model": [
        {"name": "gpt-4o", "base_url": "https://api.openai.com/v1", "api_key": os.getenv("OPENAI_API_KEY")},
        {"name": "claude-3-opus-20240229", "base_url": "https://api.anthropic.com", "api_key": os.getenv("ANTHROPIC_API_KEY")},
        {"name": "google/gemma-2-9b-it", "base_url": "https://api.albert.fr/v1", "api_key": os.getenv("ALBERT_API_KEY")},
        {"name": "meta-llama/Llama-3.1-8B-Instruct", "base_url": "https://api.albert.fr/v1", "api_key": os.getenv("ALBERT_API_KEY")},
    ],
}

# Create the experiment set with CV schema
expset = {
    "name": expset_name,
    "readme": expset_readme,
    "cv": {
        "common_params": common_params, 
        "grid_params": grid_params, 
        "repeat": 3  # Run each combination 3 times to measure variability
    }
}

# Launch the experiment set
response = requests.post(f'{API_URL}/experiment_set', json=expset, headers=HEADERS)
expset_id = response.json()["id"]
print(f"Experiment set {expset_id} is running")
```

In this example:
- `common_params` defines parameters shared across all experiments
- `grid_params` defines parameters that will vary (creating a separate experiment for each combination)
- `repeat` specifies how many times to repeat each experiment (useful for measuring variability)

The API will automatically generate experiments for all combinations of parameters in the grid.

### Manually Defining Experiments

For more control, you can explicitly define each experiment in the set:

```python
import os
import requests

# Replace with your Evalap API endpoint
API_URL = "https://evalap.etalab.gouv.fr/v1"

# Replace with your API key or authentication token
HEADERS = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

# Define your experiment set with explicit experiments
expset = {
    "name": "custom_evaluation_set",
    "readme": "Custom evaluation with different configurations for each model.",
    "experiments": [
        {
            "name": "gpt4o_standard",
            "dataset": "qa_benchmark_v2",
            "model": {
                "name": "gpt-4o", 
                "base_url": "https://api.openai.com/v1", 
                "api_key": os.getenv("OPENAI_API_KEY"),
                "sampling_params": {"temperature": 0.0}
            },
            "metrics": ["judge_precision", "output_length"]
        },
        {
            "name": "gpt4o_creative",
            "dataset": "qa_benchmark_v2",
            "model": {
                "name": "gpt-4o", 
                "base_url": "https://api.openai.com/v1", 
                "api_key": os.getenv("OPENAI_API_KEY"),
                "sampling_params": {"temperature": 0.7}
            },
            "metrics": ["judge_precision", "output_length"]
        },
        {
            "name": "llama3_with_rag",
            "dataset": "qa_benchmark_v2",
            "model": {
                "name": "meta-llama/Llama-3.1-8B-Instruct",
                "base_url": "https://api.custom.fr/v1",
                "api_key": os.getenv("CUSTOM_API_KEY"),
                "extra_params": {"rag": {"mode": "rag", "limit": 5}}
            },
            "metrics": ["judge_precision", "output_length", "contextual_relevancy"]
        }
    ]
}

# Launch the experiment set
response = requests.post(f'{API_URL}/experiment_set', json=expset, headers=HEADERS)
expset_id = response.json()["id"]
print(f"Experiment set {expset_id} is running")
```

This approach gives you complete flexibility to customize each experiment independently.

## Advanced Use Cases

Experiment sets are particularly valuable for:

1. **Model comparison**: Evaluate multiple models on the same dataset to identify the best performer
2. **Hyperparameter tuning**: Test how parameters like temperature affect model outputs
3. **Robustness testing**: Run the same experiment multiple times to measure consistency
4. **Feature evaluation**: Compare models with and without features like RAG to measure impact

## Viewing Experiment Set Results

After launching an experiment set:

1. Navigate to the experiment set details page
2. View summary results showing:
   - Comparative performance across all experiments
   - Statistical measures of variability when using repeated runs
3. Explore detailed results for individual experiments
4. Generate comparison charts and visualizations

Experiment sets provide a comprehensive view of model performance, making it easier to draw meaningful conclusions from your evaluations.


:::tip Next Steps: Experiment Sets
[Explore the notebooks for real examples of creating evaluations with experiment sets.](https://github.com/etalab-ia/evalap/tree/main/notebooks)
:::
