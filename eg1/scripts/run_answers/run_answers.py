#!/usr/bin/env python

"""
Generate output/answers with eg1 dataset with the given model.

Usage:
    run_answers.py --base-url=<url> --model=<model> --dataset=<dataset> [--auth-token=<token>] [--system-prompt=<prompt>] [--sampling-params=<params>] [--extra-params=<params>] [--max-workers=<n>] [--eg1-token=<token>]

Options:
    --base-url=<url>              Base URL for the API.
    --auth-token=<token>          Authorization token for OPENAI-API access.
    --eg1-token=<token>           Authorization token for EG1-API access.
    --model=<model>               Name of the model to use.
    --dataset=<dataset>           Name of the dataset to process.
    --system-prompt=<prompt>      Optional system prompt.
    --sampling-params=<params>    Optional sampling parameters as JSON string.
    --extra-params=<params>       Optional extra parameters as JSON string.
    --max-workers=<n>             Maximum number of concurrent requests [default: 8].
    -h --help                     Show this help message and exit.
"""

import asyncio
import concurrent.futures
import json
import os
import time
from io import StringIO

import aiohttp
import pandas as pd
import requests
from docopt import docopt

from eg1.mcp import multi_step_generate


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
        result, steps = multi_step_generate(
            model_base_url=model_base_url,
            model_api_key=model_api_key,
            model_name=model_name,
            messages=messages,
            sampling_params=sampling_params,
            mcp_bridge=None,
        )

        answer = result.choices[0].message.content

        result["success"] = True
        result["output"] = answer
    except Exception as e:
        result["error"] = str(e)
    finally:
        result["execution_time"] = time.time() - start_time

    return result


async def run_model(args):
    """Main function to process the entire dataset."""
    base_url = args["--base-url"].rstrip("/")
    model = args["--model"]
    dataset_name = args["--dataset"]
    auth_token = args["--auth-token"] or os.getenv("OPENAI_API_KEY")
    eg1_token = args["--eg1-token"] or os.getenv("EG1_API_KEY")
    system_prompt = args["--system-prompt"]
    sampling_params = args["--sampling-params"]
    extra_params = args["--extra-params"]
    max_workers = int(args["--max-workers"])

    # Get the dataset
    response = requests.get(
        f"https://eg1.dev.etalab.gouv.fr/v1/dataset?name={dataset_name}&with_df=true",
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
        results_df.to_json(f"results/{dataset_name}_processed.json", orient="records", indent=2)
        print(f"Processing complete. Results saved to results/{dataset_name}_processed.json")


def main():
    args = docopt(__doc__)
    asyncio.run(run_model(args))


if __name__ == "__main__":
    main()
