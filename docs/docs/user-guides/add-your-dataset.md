---
sidebar_position: 1
---

# Add Your Dataset

This guide will walk you through the process of adding a new dataset to Evalap for model evaluation.

## Dataset Requirements

Before adding a dataset, ensure it meets the following requirements:

- The dataset should be in a supported format (JSON, CSV, or JSONL)
- Each entry in the dataset should contain at least:
  - An input field (the prompt or question)
  - A reference field (the expected output or answer)

## Adding a Dataset via the Web Interface

1. Log in to the Evalap web interface
2. Navigate to the "Datasets" section
3. Click on the "Add New Dataset" button
4. Fill in the required information:
   - Dataset name
   - Description
   - Tags (optional)
5. Upload your dataset file
6. Map the fields in your dataset to the required fields in Evalap
7. Click "Submit" to add your dataset

## Adding a Dataset via the API

You can also add a dataset programmatically using the Evalap API:

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

# Prepare dataset metadata
dataset_metadata = {
    "name": "My Custom Dataset",
    "description": "A dataset for evaluating question answering capabilities",
    "tags": ["question-answering", "french"]
}

# Create the dataset
response = requests.post(
    f"{API_URL}/datasets",
    headers=HEADERS,
    json=dataset_metadata
)

dataset_id = response.json()["id"]

# Now upload the dataset file
with open("my_dataset.json", "rb") as f:
    files = {"file": ("my_dataset.json", f, "application/json")}
    response = requests.post(
        f"{API_URL}/datasets/{dataset_id}/upload",
        headers={"Authorization": HEADERS["Authorization"]},
        files=files
    )

print(f"Dataset uploaded: {response.json()}")
```

## Dataset Format Example

Here's an example of a properly formatted dataset in JSON:

```json
[
  {
    "question": "What is the capital of France?",
    "answer": "Paris",
    "category": "Geography",
    "difficulty": "Easy"
  },
  {
    "question": "Who wrote 'Les Misérables'?",
    "answer": "Victor Hugo",
    "category": "Literature",
    "difficulty": "Medium"
  }
]
```

When mapping this dataset in Evalap, you would map:
- "question" to the input field
- "answer" to the reference field

The additional fields ("category" and "difficulty") can be used for filtering and analysis.

## Next Steps

After adding your dataset, you can:

- [Create a simple experiment](./create-a-simple-experiment.md) using your dataset
- Add more datasets for comprehensive evaluation
- Explore existing datasets in the platform
