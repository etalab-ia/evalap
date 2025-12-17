---
sidebar_position: 3
---


# Evaluate you own IA system


You can use EvalAP for its evaluation component.

How it works:
- Your AI system generates its responses (and additional metadata if necessary) on your evaluation dataset.
- You send these generations to EvalAP and create an experiment at the same time. EvalAP calculates the requested metrics.
- You can see the results on the frontend.

Notes: You must have loaded the evaluation dataset once into EvalAP via the dataset endpoint.

---

## 1- Generation of responses by your AI system
 Your AI system generates responses in a dataframe 'res_for_evalap'

## 2- Use EvalAP to obtain the evaluation metrics

```python

import os
import json
import requests
import pandas as pd

#config
API_URL = "http://localhost:8000/v1"
EVALAP_API_KEY = os.getenv("EVALAP_API_KEY")
headers = {"Authorization": f"Bearer {EVALAP_API_KEY}"}
```


### 2.1  Post dataset
This step only needs to be done once.

```python
def post_dataset_to_api(name, readme, df, default_metric, columns_map=None, compliance=False):
    dataset_payload = {
        "name": name,
        "readme": readme,
        "default_metric": default_metric,
        "df": df.to_json(orient="records"),
        "compliance": compliance
    }
    if columns_map:
        dataset_payload["columns_map"] = columns_map
    try:
        response = requests.post(f"{API_URL}/dataset", json=dataset_payload, headers=headers)
        response.raise_for_status()
        resp = response.json()
        if "id" in resp:
            print(f"Dataset '{name}' publié avec succès (ID: {resp['id']})")
        else:
            print(f"Erreur de publication pour '{name}': {resp}")
    except requests.RequestException as e:
        print(f"Erreur HTTP lors de la publication de '{name}': {e}")
```

dataset is a df that contains :  "question", "ground_truth" (and other columns)

```python
post_dataset_to_api(
    name="assistant",
    readme="'assistant -- test",
    df=dataset,
    default_metric="judge_notator",
    columns_map={"query": "question", "output_true" : "ground_truth"},
    compliance=False
)
```

### 2.2  Run Eval
First RUN -- You have not completed an assessment on this AI system.

res_for_evalap contains "answer", "generation_time", "contexts" (in this example)

```python

products = "assistant-"
dataset_name = "assistant"

judge_name = "gpt-4.1"
judge_api_url = "https://api.openai.com/v1",
judge_api_key = os.getenv("OPENAI_API_KEY")

expset_name = f"{products}_run_{judge_name}"
expset_readme = f"evals for perfomring IA system of {products}"

metrics = ["judge_notator", "faithfulness", "answer_relevancy"]

common_params = {
    "dataset": dataset_name,
    "metrics": metrics,
    "judge_model": {
        "name": judge_name,
        "base_url": judge_api_url,
        "api_key": judge_api_key,
},
}
grid_params = {
    "model": [
        {
            "aliased_name": "IA-system",
            "output":res_for_evalap["answer"].values.tolist(),
        },
    ]
}

expset = {
    "name": expset_name,
    "readme": expset_readme,
    "cv": {"common_params": common_params, "grid_params": grid_params, "repeat": 1},
}

response = requests.post(f"{API_URL}/experiment_set", json=expset, headers=headers)
resp = response.json()
if "id" in resp:
    print(f'Created expset: {resp["name"]} (ID: {resp["id"]})')
else:
    print(f'Error creating experiment set for {dataset_name}: {resp}')

```

Patch -- You have already completed at least one assessment on this AI system, and you want to complete new ones in the same place.
You must then enter the experiment number in the patch.

```python
# Patching the experiment set

output_list = res_for_evalap["answer"].astype(str).tolist()
time_list = res_for_evalap["generation_time"].astype(int).values.tolist()
nb_tokens_completion = res_for_evalap["generation_time"].astype(int).values.tolist()
#format context for EvalAP
context_raw = res_for_evalap["contexts"].astype(str).tolist()
context_formatted = [[item] for item in context_raw]

expset_id = 181

metrics = ["judge_precision", "judge_notator", "judge_exactness",  "answer_relevancy",
           "faithfulness", "contextual_precision", "contextual_recall", "contextual_relevancy"]
           # "ragas"   ragas is no longer supported in deepeval

common_params = {
    "dataset" : dataset_name,
    "model": {"sampling_params" : {"temperature": 0.2}},
    "metrics" : metrics,
    "judge_model": {
        "name": judge_name,
        "base_url": judge_api_url,
        "api_key": judge_api_key,
},
}

grid_params = {
    "model": [
        {
            "aliased_name": "IA-system_+metrics",
            "output": json.loads(json.dumps(output_list)),
            "execution_time": time_list,
            "nb_tokens_completion": nb_tokens_completion,
            #"nb_tokens_prompt": nb_tokens_prompt,
            "retrieval_context": context_formatted #list of list
            #"context": context_formatted #list of list
        },
    ]
}

expset = {
    "cv": {"common_params": common_params, "grid_params": grid_params, "repeat":1}
}
response = requests.patch(f'{API_URL}/experiment_set/{expset_id}', json=expset, headers=headers)
resp = response.json()
if "id" in resp:
    expset_id = resp["id"]
    print(f'Patched expset: {resp["name"]} ({resp["id"]})')
else:
    print(resp)
```

You can now see the result in the front : http://localhost:8501/experiments_set
