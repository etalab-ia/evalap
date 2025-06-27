#!/usr/bin/env python

"""
Generate output/answers with eg1 dataset with the given model.

Usage:
    run_answers.py --run-name=<name> --base-url=<url> --model=<model> --dataset=<dataset> [--auth-token=<token>] [--system-prompt=<prompt>] [--sampling-params=<params>] [--extra-params=<params>] [--max-workers=<n>] [--eg1-token=<token>] [--repeat=<n>]

Options:
    --run-name=<name>             name of this model generation.
    --base-url=<url>              Base URL for the API.
    --auth-token=<token>          Authorization token for OPENAI-API access.
    --eg1-token=<token>           Authorization token for EG1-API access.
    --model=<model>               Name of the model to use.
    --dataset=<dataset>           Name of the dataset to process.
    --system-prompt=<prompt>      Optional system prompt.
    --sampling-params=<params>    Optional sampling parameters as JSON string.
    --extra-params=<params>       Optional extra parameters as JSON string.
    --max-workers=<n>             Maximum number of concurrent requests [default: 8].
    --repeat=<n>                  number of repetition of the run (number if file generated) [default: 1].
    -h --help                     Show this help message and exit.

Examples:
    eg1_generate_answers --base-url http://localhost:9191/v1 --model google/gemma-3-27b-it --dataset MFS_questions_v01 --repeat 4 --run-name gemma-3-27b_mfs
"""

import concurrent.futures
import json
import os
import time
from io import StringIO

import pandas as pd
import requests
from docopt import docopt

from eg1.clients import multi_step_generate

eg1_url = "https://eg1.etalab.gouv.fr/v1"


def process_query(
    row,
    model_base_url: str,
    model_api_key: str,
    model_name: str,
    system_prompt=None,
    sampling_params=None,
    extra_params=None,
):
    """Process a single query against the model."""

    messages = [{"role": "user", "content": row["query"]}]
    if system_prompt:
        messages = [{"role": "system", "content": system_prompt}] + messages

    if extra_params:
        # @TODO catch _tools_
        pass

    start_time = time.time()
    result = {
        "num_line": row.name,
        "success": False,  # Default to False, will update if successful
        "execution_time": 0,  # Will be updated at the end
        "query": row["query"],
        "output": None,
        "error": None,
    }

    try:
        r, steps = multi_step_generate(
            model_base_url=model_base_url,
            model_api_key=model_api_key,
            model_name=model_name,
            messages=messages,
            sampling_params=sampling_params or {},
            mcp_bridge=None,
        )
        answer = r.choices[0].message.content
        result["success"] = True
        result["output"] = answer
    except Exception as e:
        result["error"] = str(e)
    finally:
        result["execution_time"] = time.time() - start_time

    return result


def run_model(args):
    """Main function to process the entire dataset."""
    run_name = args["--run-name"]
    base_url = args["--base-url"].rstrip("/")
    model = args["--model"]
    dataset_name = args["--dataset"]
    auth_token = args["--auth-token"] or os.getenv("OPENAI_API_KEY")
    eg1_token = args["--eg1-token"] or os.getenv("EG1_API_KEY")
    system_prompt = args["--system-prompt"]
    sampling_params = args["--sampling-params"]
    if sampling_params:
        try:
            sampling_params = json.loads(sampling_params)
        except json.JSONDecodeError as e:
            print(f"Error parsing sampling_params: {e}")
            return
    extra_params = args["--extra-params"]
    if extra_params:
        try:
            extra_params = json.loads(extra_params)
        except json.JSONDecodeError as e:
            print(f"Error parsing extra_params: {e}")
            return
    max_workers = int(args["--max-workers"])
    repeat = int(args["--repeat"])

    # Get the dataset
    response = requests.get(
        f"{eg1_url}/dataset?name={dataset_name}&with_df=true",
        headers={"Authorization": f"Bearer {eg1_token}"},
    )
    response.raise_for_status()
    dataset = response.json()

    # Parse the dataframe
    df = pd.read_json(StringIO(dataset["df"]))
    if "query" not in df.columns:
        print("Error: Dataframe doesn't have a 'query' column")
        return

    print(f"Successfully loaded dataset `{dataset['name']}` with {len(df)} queries")
    print(f"model: {model}")
    print(f"sampling_params: {sampling_params}")
    model_raw = {
        "aliased_name": model,
        "name": model,
        "base_url": base_url,
        "system_prompt": system_prompt,
        "sampling_params": sampling_params,
        "dataset": dataset["name"],
    }

    with open(f"results/{run_name}__details.json", "w") as f:
        json.dump(model_raw, f, indent=2)

    for repetition in range(repeat):
        print(f"run {repetition}/{repeat}")
        results = []
        start_time = time.time()
        # Create a thread pool for parallel processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks to the executor
            futures = [
                executor.submit(
                    process_query,
                    row,
                    base_url,
                    auth_token,
                    model,
                    system_prompt,
                    sampling_params,
                    extra_params,
                )
                for _, row in df.iterrows()
            ]

            # Collect results as they complete
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                result = future.result()
                results.append(result)
                elapsed = time.time() - start_time
                print(
                    f"Progress: {i + 1}/{len(df)} ({((i + 1) / len(df)) * 100:.1f}%) - Elapsed: {elapsed:.2f}s",
                    end="\r",
                    flush=True,
                )

            # Combine results with original dataframe
            results_df = pd.DataFrame(results)

            # Save results
            os.makedirs("results", exist_ok=True)
            results_df.to_json(
                f"results/{run_name}__{repetition}.json",
                orient="records",
                indent=2,
                force_ascii=False,
            )
            print(f"Processing complete. Results saved to results/{run_name}__{repetition}.json")


def main():
    args = docopt(__doc__)
    run_model(args)


if __name__ == "__main__":
    main()
