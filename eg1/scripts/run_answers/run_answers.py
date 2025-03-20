#!/usr/bin/env python

"""
Generate output/answers with eg1 dataset with the given model.

Usage:
    run_answers.py --base-url=<url> --model=<model> --dataset=<dataset> [--auth-token=<token>] [--system-prompt=<prompt>] [--sampling-params=<params>] [--max-concurrent=<n>]

Options:
    --base-url=<url>              Base URL for the API.
    --auth-token=<token>          Authorization token for OPENAI-API access.
    --eg1-token=<token>           Authorization token for EG1-API access.
    --model=<model>               Name of the model to use.
    --dataset=<dataset>           Name of the dataset to process.
    --system-prompt=<prompt>      Optional system prompt.
    --sampling-params=<params>    Optional sampling parameters as JSON string.
    --max-concurrent=<n>          Maximum number of concurrent requests [default: 8].
    -h --help                     Show this help message and exit.
"""

import asyncio
from io import StringIO
import json
import os
import time

import aiohttp
import pandas as pd
import requests
from docopt import docopt


async def process_query(
    session,
    base_url,
    model,
    row,
    system_prompt=None,
    sampling_params=None,
    extra_params=None,
    auth_token=None,
):
    """Process a single query against the model."""

    messages = [{"role": "user", "content": row["query"]}]
    if system_prompt:
        messages = [{"role": "system", "content": model.prompt_system}] + messages

    payload = {
        "model": model,
        "messages": messages,
    }

    if sampling_params:
        try:
            sampling_dict = json.loads(sampling_params)
            payload.update(sampling_dict)
        except json.JSONDecodeError:
            print(f"Warning: Could not parse sampling parameters: {sampling_params}")

    if extra_params:
        # @TODO catch _tools_
        try:
            sampling_dict = json.loads(extra_params)
            payload.update(sampling_dict)
        except json.JSONDecodeError:
            print(f"Warning: Could not parse sampling parameters: {sampling_params}")

    headers = {"Content-Type": "application/json"}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

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
        async with session.post(
            f"{base_url}/v1/completions", headers=headers, json=payload
        ) as response:
            response = await response.json()

            if response.status == 200:
                result["success"] = True
                result["output"] = response["choices"][0]["message"]["content"]
            else:
                result["error"] = f"HTTP {response.status}: {response}"
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
    max_concurrent = int(args["--max-concurrent"])

    # Get the dataset
    response = requests.get(
        f"{base_url}/v1/dataset?name={dataset_name}&with_df=true", headers=f"Bearer {eg1_token}"
    )
    response.raise_for_status()
    dataset = response.json()

    # Parse the dataframe
    df = pd.read_json(dataset["df"])
    if "query" not in df.columns:
        print("Error: Dataframe doesn't have a 'query' column")
        return

    print(f"Successfully loaded dataset `{dataset['name']}` with {len(df)} queries")

    # Setup session for HTTP requests
    async with aiohttp.ClientSession() as session:
        # Process queries with concurrency limit
        semaphore = asyncio.Semaphore(max_concurrent)
        results = []

        async def process_with_semaphore(row):
            async with semaphore:
                # print(f"Processing row: {row.name}...")
                result = await process_query(
                    session,
                    base_url,
                    model,
                    row,
                    system_prompt,
                    sampling_params,
                    extra_params,
                    auth_token,
                )
                return result

        tasks = [process_with_semaphore(row) for _, row in df.iterrows()]
        start_time = time.time()
        for i, future in enumerate(asyncio.as_completed(tasks)):
            result = await future
            results.append(result)
            elapsed = time.time() - start_time
            print(
                f"Progress: {i + 1}/{len(tasks)} ({((i + 1) / len(tasks)) * 100:.1f}%) - Elapsed: {elapsed:.2f}s",
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
