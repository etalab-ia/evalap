---
sidebar_position: 7
title: LLM Compliance Evaluation Workflows
---

# LLM Compliance Evaluation Workflows
## Objectives and Scope

This page explains how to analyze and compare the compliance performance of various large language models (LLMs) using EvalAP, with a focus on ethical dimensions, social biases, and toxicity. It will guide you through standard metrics, datasets, and provide Python code to publish your datasets and run systematic evaluations.
Each dataset and metric is chosen to reflect specific compliance challenges and their practical relevance.

---

### Datasets and Benchmarks

Below is a summary of the main datasets used to evaluate LLM compliance. Each one tests a particular area of responsible AI behavior:

| Dataset Used            | Main Evaluation Objective                          | Key Metrics                      | Notes                                           |
|-------------------------|---------------------------------------------------|---------------------------------|-------------------------------------------------|
| **llm-values/CIVICS**   | Cultural sensitivity and value variation          | `bias`| Measures cultural coherence and neutrality     |
| **lmsys-toxic-chat**    | Toxicity in LLM generations                        | `toxicity`  `bias`     | Ensures moderation, detects unsafe outputs     |
| **crows-pairs**         | Implicit linguistic and social biases              | `bias`  | Ensures robustness against stereotypes         |
| **DECCP**               | Censorship (focus on China-related topics)         | `toxicity`  `bias`      | Detects censorship in Chinese content          |


---

### Compliance Metrics: How to Interpret

| Metric                 | Description                                        | Desired Outcome                              |
|------------------------|---------------------------------------------------|----------------------------------------------|
| `bias`             | Social/ethnic bias in generation                  | Prefer low values for neutrality              |
| `toxicity`          | Offensive, discriminatory, harmful content        | Low score required for ethical compliance    |

Additional technical indicators can be attached for operational monitoring:

| Metric              | Description                                        |
|------------------------|---------------------------------------------------|
| `generation_time`      | Time taken to generate an answer                  |
| `nb_tokens_prompt` `nb_tokens_completion` | Token volume processed in prompts/completions   |
| `energy_consumption`   | Inference energy usage                             |
| `gwp_consumption`      | Carbon impact (Global Warming Potential)          |

---

## Compliance assessment campaign cost alert

These datasets contain numerous questions. Launching a compliance campaign can be costly. We recommend:
- performing stratified sampling to reduce the number of questions while retaining the information contained
- setting repeat to a maximum of 3
- using a mini-type judge

---

## Example: run Compliance
Here are typical approaches to prepare and publish datasets for compliance evaluation on EvalAP.

### Load and Publish Datasets


```python

import os
import sys
import time

from datasets import load_dataset
import dotenv
from IPython.display import HTML
import pandas as pd
import requests

dotenv.load_dotenv("../.env")
sys.path.append("..")

# Replace with your Evalap API key and endpoint
EVALAP_API_URL = "http://localhost:8000/v1"
EVALAP_API_KEY = os.getenv("EVALAP_API_KEY")

HEADERS = {
    "Authorization": "Bearer {EVALAP_API_KEY}",
    "Content-Type": "application/json"
}

# Load the dataset from a CSV file
def load_crows_pairs(filepath: str) -> pd.DataFrame:
    df_crows_pairs = pd.read_csv(filepath)
    df_crows_more = df_crows_pairs[['sent_more']].rename(columns={'sent_more': 'query'})
    df_crows_less = df_crows_pairs[['sent_less']].rename(columns={'sent_less': 'query'})
    df_crows = pd.concat([df_crows_more, df_crows_less], ignore_index=True)
    return df_crows

def load_hf_dataset(hf_path, split, hf_kwargs=None):
    try:
        ds = load_dataset(hf_path, split=split, **(hf_kwargs or {}))
    except Exception:
        ds = load_dataset(hf_path, split=split, download_mode="reuse_cache_if_exists", **(hf_kwargs or {}))
    return ds.to_pandas()

def post_dataset_to_api(name, readme, df, default_metric, columns_map=None, compliance=True):
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
        response = requests.post(f"{EVALAP_API_URL}/dataset", json=dataset_payload, headers=headers)
        response.raise_for_status()
        resp = response.json()
        if "id" in resp:
            print(f"Dataset '{name}' publié avec succès (ID: {resp['id']})")
        else:
            print(f"Erreur de publication pour '{name}': {resp}")
    except requests.RequestException as e:
        print(f"Erreur HTTP lors de la publication de '{name}': {e}")

#  datasets HuggingFace
df_civics = load_hf_dataset("llm-values/CIVICS", split="test")
df_toxic_chat = load_hf_dataset("lmsys/toxic-chat", split="train", hf_kwargs={"name": "toxicchat1123"})

#  dataset Crows pairs (https://github.com/nyu-mll/crows-pairs/tree/master/data)
df_crows = load_crows_pairs('_data/crows_pairs_anonymized.csv')

#Publish
post_dataset_to_api(
    name="llm-values-CIVICS",
    readme="'Culturally-Informed & Values-Inclusive Corpus for Societal Impacts' is a dataset designed to evaluate the social and cultural variation of Large Language Models (LLMs) towards socially sensitive topics across multiple languages and cultures.",
    df=df_civics,
    default_metric="bias",
    columns_map={"query": "Statement"},
    compliance=True
)

post_dataset_to_api(
    name="lmsys-toxic-chat",
    readme="This dataset contains toxicity annotations on 10K user prompts collected from the Vicuna online demo.",
    df=df_toxic_chat,
    default_metric="toxicity",
    columns_map={"query": "user_input"},
)

post_dataset_to_api(
    name="crows-pairs",
    readme="Dataset crows pairs with anonymized sentences for bias evaluation. License: Creative Commons Attribution-ShareAlike 4.0 International License.",
    df=df_crows,
    default_metric="bias",
    columns_map={"query": "query"},
)

```

---

### Define your Compliance experiment
In this example:
- `datasets_metrics` defines the associated metrics and impact for each dataset
- `common_params` defines parameters shared across all experiments
- `grid_params` defines parameters that will vary (creating a separate experiment for each combination)
- `repeat` specifies how many times to repeat each experiment (useful for measuring variability)


```python
products = "MY_PRODUCT_NAME"
JUDGE = "gpt-5-mini"

# Common technical metrics
technical_metrics = [
    "generation_time",
    "nb_tokens_prompt",
    "nb_tokens_completion",
    "energy_consumption",
    "gwp_consumption",
]

datasets_metrics = {
    "llm-values-CIVICS": {
        "metrics": ["bias", "answer_relevancy", "faithfulness"],
        "impact_type": "Cultural_and_social_values"
    },
    "lmsys-toxic-chat": {
        "metrics": ["toxicity", "bias", "answer_relevancy"],
        "impact_type": "Toxicity"
    },
    "crows-pairs": {
        "metrics": ["bias", "answer_relevancy", "faithfulness"],
        "impact_type": "Social_biases"
    }
}


for dataset_name, info in datasets_metrics.items():
    expset_name = f"{products}_base_on_{info['impact_type']}"
    expset_readme = f"Compliance Evaluation for {products} Product, based on {dataset_name} dataset, who analyze {info['impact_type']}"

    metrics = info["metrics"] + technical_metrics

    common_params = {
        "dataset": dataset_name,
        "model": {
            "extra_params": {"rag": {"mode": "rag", "limit": 7}},
            "sampling_params": {"temperature": 0.2},
        },
        "metrics": metrics,
        "judge_model": JUDGE,
    }
    grid_params = {
        "model": [
            {
                "name": "mistralai/Mistral-Small-3.2-24B-Instruct-2506",
                "aliased_name": "albert-large",
                "base_url": "https://api.albert.fr/v1", "api_key": os.getenv("ALBERT_API_KEY")
            },
            {
                "name": "meta-llama/Llama-3.1-8B-Instruct",
                "aliased_name": "albert-small",
                "base_url": "https://api.albert.fr/v1", "api_key": os.getenv("ALBERT_API_KEY")
            },
        ]
    }
    # Create the experiment set
    expset = {
        "name": expset_name,
        "readme": expset_readme,
        "cv": {"common_params": common_params, "grid_params": grid_params, "repeat": 3},
    }

    # Launch the experiment set
    response = requests.post(f"{EVALAP_API_URL}/experiment_set", json=expset, headers=headers)
    resp = response.json()
    if "id" in resp:
        print(f'Created expset: {resp["name"]} (ID: {resp["id"]})')
    else:
        print(f'Error creating experiment set for {dataset_name}: {resp}')


```



## Viewing Experiment Results and Progress

After launching an experiment:

1. Navigate to the compliance details page : http://localhost:8501/compliance
2. View summary results showing:
   - Overall performance metrics for each model
   - Support table displaying the number of experiments used for score averaging
3. Explore detailed results:
   - Number of successful and failed attempts per experiment
   - Detailed results for each experiment

:::tip Next Steps:
[Explore the notebooks for real examples of creating evaluations with EvalAP.](https://github.com/etalab-ia/evalap/tree/main/notebooks)
:::
