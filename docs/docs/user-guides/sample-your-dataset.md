---
sidebar_position: 5
---

# Sample your dataset

This guide will walk you through how to use the sampling feature.
See the [api reference](https://evalap.etalab.gouv.fr/redoc#tag/experiment_set/operation/create_experimentset_v1_experiment_set_post) for more usage detail.

You must retrieve your dataset:

```python
import os
import requests
import json
import pandas as pd

# Replace with your Evalap API endpoint
API_URL = "http://localhost:8000/v1"
EVALAP_API_KEY = os.getenv("EVALAP_API_KEY")

# Replace with your API key or authentication token (or None if launch locally)
HEADERS = {
    "Authorization": "Bearer EVALAP_API_KEY",
    "Content-Type": "application/json"
}

judge_name = "gpt-4.1"
judge_api_url = "https://api.openai.com/v1",
judge_api_key = os.getenv("OPENAI_API_KEY")

# Fetch the dataset from Evalap
# --
dataset_name = <YOUR_DATASET_NAME>
response = requests.get(
    f"{EVALAP_API_URL}/dataset?name={dataset_name}&with_df=true",
    headers={"Authorization": f"Bearer {EVALAP_API_KEY}"},
)
response.raise_for_status()
dataset = response.json()
dataset_df =  pd.read_json(StringIO(dataset["df"]))
dataset_df
```

Then, you can use sample method:

```python
# Build 1000 random index to work with a subset of the dataset in order to do faster and cheaper evaluation
# --
N = len(dataset_df) # Size of the dataset
rng = np.random.default_rng(42)
sample = rng.choice(np.arange(N), size=1000, replace=False)
sample = sample.tolist()
```

and pass the sample in your experimentset like this:


```python
common_params = {
    "dataset": dataset["name"],
    "metrics": metrics_list,
    "model": {"sampling_params" : sampling_params, "system_prompt": system_prompt},
    "judge_model": {
        "name": JUDGE_NAME, "base_url": JUDGE_API_URL, "api_key": JUDGE_API_KEY
    },
    "sample": sample,
}

```
