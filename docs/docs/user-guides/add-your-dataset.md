---
sidebar_position: 1
---

# Publish a Dataset

This guide will walk you through the process of adding a new dataset to Evalap for model evaluation.
You can add a dataset programmatically using the Evalap API.

Two formats are supported :

- CSV like data (dataframes)
- Parquet format (for bigger dataset)


## Column Mapping


Evalap uses a standard column naming convention. When adding your dataset, you need to either name your columns accordingly or map your dataset columns to these standard names using the `columns_map` parameter:

- `query`: (str) the input query.
- `output`: (str) the model answer.
- `output_true`: (str) the ground truth answer.
- `context`: list[str] a list of contextual information pass to the prompt.
- `retrieval_context`: list[str] a list of retrieved information pass to the prompt.
- `reasoning`: (str) The reasoning output tokens associated to an answer.
- (to come) `tools_called`
- (to come) `expected_tools`


If the column names of your dataset do not match these conventions, you can either rename them before adding the dataset, or use the parameter `columns_map` in the request to provide a mapping between the Evalap convention names and yours.



For example, if your dataset has columns named "question" and "answer", you would map them like this:

```json
"columns_map": {"input": "question", "output": "answer"}
```

See the [api reference](https://evalap.etalab.gouv.fr/redoc#tag/datasets/operation/create_dataset_v1_dataset_post) for more usage detail.


## From CSV like dataset

The following code show how to upload a dataset to Evalap from a CSV file.

```python
import requests
import json
import pandas as pd

# Replace with your Evalap API endpoint
API_URL = "https://evalap.etalab.gouv.fr/v1"

# Replace with your API key or authentication token (or None if launch locally)
HEADERS = {
    "Authorization": "Bearer YOUR_EVALAP_KEY",
    "Content-Type": "application/json"
}

# Load the dataset from a CSV file
dataset_df = pd.read_csv("my_dataset.csv")  # Pandas use "," as default limiter.


# Prepare dataset metadata
dataset = {
    "name": "My domain specific dataset",
    "readme": "A dataset for evaluating question answering capabilities",
    "default_metric": "judge_precision",
    "df": dataset_df.to_json()
}

# Create the dataset
response = requests.post( f"{API_URL}/datasets", headers=HEADERS, json=dataset)

dataset_id = response.json()["id"]

print(f"Dataset created with ID: {dataset_id}")
```


## From Parquet Dataset

See the demo tutorial to add an OCR dataset provided by the Marker library: [create_marker_dataset.ipynb](https://github.com/etalab-ia/evalap/blob/main/notebooks/create_marker_dataset.ipynb)


## Next Steps

After adding your dataset, you can:

- [Create a simple experiment](./create-a-simple-experiment.md) using your dataset
- Explore existing datasets in the platform
