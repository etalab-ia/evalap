---
sidebar_position: 2
---

# Create a Simple Experiment

This guide will walk you through the process of creating and running a simple evaluation experiment in Evalap.

## Prerequisites

Before creating an experiment, ensure you have:

- Access to the Evalap platform
- At least one dataset added to the platform
- Access to one or more models for evaluation

## Creating an Experiment via the Web Interface

1. Log in to the Evalap web interface
2. Navigate to the "Experiments" section
3. Click on the "Create New Experiment" button
4. Fill in the experiment details:
   - Experiment name
   - Description
   - Tags (optional)
5. Select the dataset(s) you want to use for evaluation
6. Select the model(s) you want to evaluate
7. Choose the evaluation metrics:
   - Accuracy
   - F1 Score
   - BLEU Score
   - ROUGE Score
   - Custom metrics (if available)
8. Configure experiment parameters:
   - Number of samples (or use the entire dataset)
   - Randomization seed (for reproducibility)
   - Parallel execution settings
9. Click "Create Experiment" to save your configuration
10. Click "Run Experiment" to start the evaluation

## Creating an Experiment via the API

You can also create and run experiments programmatically using the Evalap API:

```python
import requests
import json

# Replace with your Evalap API endpoint
API_URL = "https://evalap.etalab.gouv.fr/api"

# Replace with your API key or authentication token
HEADERS = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

# Prepare experiment configuration
experiment_config = {
    "name": "Simple QA Evaluation",
    "description": "Evaluating model performance on question answering",
    "datasets": ["dataset_id_1"],  # Replace with actual dataset IDs
    "models": ["model_id_1", "model_id_2"],  # Replace with actual model IDs
    "metrics": ["accuracy", "f1_score"],
    "parameters": {
        "sample_size": 100,  # Number of samples to use
        "seed": 42,  # Random seed for reproducibility
        "max_parallel_requests": 5  # Number of parallel requests
    }
}

# Create the experiment
response = requests.post(
    f"{API_URL}/experiments",
    headers=HEADERS,
    json=experiment_config
)

experiment_id = response.json()["id"]

# Run the experiment
response = requests.post(
    f"{API_URL}/experiments/{experiment_id}/run",
    headers=HEADERS
)

print(f"Experiment started: {response.json()}")

# Check experiment status
response = requests.get(
    f"{API_URL}/experiments/{experiment_id}/status",
    headers=HEADERS
)

print(f"Experiment status: {response.json()}")
```

## Monitoring Experiment Progress

Once your experiment is running, you can monitor its progress:

1. In the web interface, navigate to the "Experiments" section
2. Find your experiment in the list and click on it
3. The experiment details page will show:
   - Current status (Running, Completed, Failed)
   - Progress indicator
   - Estimated time remaining
   - Partial results (if available)

## Viewing Experiment Results

After the experiment completes:

1. Navigate to the experiment details page
2. View the summary results showing:
   - Overall performance metrics for each model
   - Comparative charts and visualizations
3. Explore detailed results:
   - Per-sample performance
   - Error analysis
   - Model output examples
4. Export results in various formats (CSV, JSON, PDF)

## Next Steps

After creating your first experiment, you can:

- Create more complex experiments with multiple datasets and models
- Customize evaluation metrics for specific use cases
- Analyze results to identify model strengths and weaknesses
- Share experiment results with your team