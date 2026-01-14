import argparse
import logging
import os
import shutil
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv
from huggingface_hub import HfApi, create_repo
from tqdm import tqdm

load_dotenv()

API_BASE_URL = "https://evalap.etalab.gouv.fr"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_json(endpoint, params=None):
    url = f"{API_BASE_URL}{endpoint}"
    headers = {"User-Agent": "EvalAP-Archiver/1.0", "Accept": "application/json"}
    token = os.getenv("EVALAP_API_KEY")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = requests.get(url, params=params, headers=headers, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching {url}: {e}")
        return None


def fetch_experiment_set_details(experiment_set_id):
    return fetch_json(f"/v1/experiment_set/{experiment_set_id}")


def fetch_experiments_with_details(experiment_set_id):
    experiments = fetch_json(
        "/v1/experiments", params={"set_id": experiment_set_id, "limit": 1000, "orphan": "false"}
    )
    if not experiments:
        return []

    full_experiments = []
    for exp in tqdm(experiments, desc=f"Fetching Exps for Set {experiment_set_id}"):
        full_exp = fetch_json(
            f"/v1/experiment/{exp['id']}",
            params={"with_results": "true", "with_answers": "true", "with_eco": "true"},
        )
        if full_exp:
            full_experiments.append(full_exp)
    return full_experiments


def check_repeat_mode(experiments):
    for expe in experiments:
        name = expe.get("name", "")
        if "__" in name and name.split("__")[-1].isdigit():
            return True
    return False


def get_dataset_dataframe(dataset_id, cache):
    if dataset_id in cache:
        return cache[dataset_id]

    ds_full = fetch_json(f"/v1/dataset/{dataset_id}", params={"with_df": "true"})
    if ds_full and ds_full.get("df"):
        try:
            df = pd.read_json(StringIO(ds_full["df"]))
            cache[dataset_id] = df
            return df
        except Exception as e:
            logger.error(f"Error parsing dataset {dataset_id} dataframe: {e}")
    cache[dataset_id] = None
    return None


def calculate_metrics_columns(exp, df):
    # Merge answers
    answers = exp.get("answers", [])
    if answers:
        answer_fields_to_show = ["answer", "error_msg", "context", "retrieval_context"]
        for field in answer_fields_to_show:
            values = {
                answer["num_line"]: answer.get(field)
                for answer in answers
                if answer.get("num_line") is not None
            }
            if any(value is not None for value in values.values()):
                field_name = "answer_" + field if not field.startswith("answer") else field
                df[field_name] = df.index.map(values)

    # Merge result scores
    results = exp.get("results", [])
    if results:
        for result in results:
            metric_name = result.get("metric_name")
            if result.get("metric_aliased_name"):
                metric_name = result["metric_aliased_name"]
            observations = {
                obs["num_line"]: obs["score"]
                for obs in result.get("observation_table", [])
                if obs.get("num_line") is not None
            }
            if observations:
                df[f"result_{metric_name}"] = df.index.map(observations)
    return df


def generate_experiment_markdown(exp, datasets_cache):
    exp_id = exp.get("id")
    exp_name = exp.get("name", str(exp_id))

    md = []
    md.append(f"# Experiment {exp_id}\n")
    md.append(f"**Name:** {exp_name}\n")
    md.append(f"**Dataset:** {exp.get('dataset', {}).get('name')}\n")
    md.append(f"**Model:** {exp.get('model', {}).get('name')}\n")
    md.append(f"**Status:** {exp.get('experiment_status')}\n")
    md.append("\n## Results\n")

    # We need to reconstruct the dataframe for this single experiment to print it as markdown
    # Note: This is slightly inefficient as we might re-fetch/re-process, but clean for isolation.
    # Optimization: passing the row from the big dataframe would be better if possible.
    # For now, let's just make a mini-df from the raw data preparation logic
    # or just print the raw results JSON if complex.

    dataset_id = exp.get("dataset", {}).get("id")
    df = None
    if dataset_id:
        # We can reuse the cache if passed from main, but for now simple fetch
        if dataset_id not in datasets_cache:
            get_dataset_dataframe(dataset_id, datasets_cache)

        base_df = datasets_cache.get(dataset_id)
        if base_df is not None:
            df = base_df.copy()
            if exp.get("sample"):
                df = df.iloc[exp.get("sample")]

            # Add metrics columns locally
            df = calculate_metrics_columns(exp, df)

            # Truncate long strings for markdown display
            for col in df.columns:
                if df[col].dtype == "object":
                    df[col] = df[col].apply(
                        lambda x: str(x)[:200] + "..." if isinstance(x, str) and len(str(x)) > 200 else x
                    )

            md.append(df.to_markdown())

    if df is None:
        md.append("No data available.")

    return "\n".join(md)


def prepare_raw_data(full_experiments):
    datasets_cache = {}
    all_rows = []

    for exp in full_experiments:
        dataset_info = exp.get("dataset")
        if not dataset_info or not dataset_info.get("id"):
            continue

        dataset_id = dataset_info["id"]
        base_df = get_dataset_dataframe(dataset_id, datasets_cache)
        if base_df is None:
            continue

        # Create a copy for this experiment
        exp_df = base_df.copy()

        # Apply sample if present
        sample = exp.get("sample")
        if sample:
            exp_df = exp_df.iloc[sample].copy()

        # Add experiment metadata columns
        exp_df["experiment_id"] = exp["id"]
        exp_df["experiment_name"] = exp.get("name")
        exp_df["model_name"] = (exp.get("model") or {}).get("name")
        exp_df["dataset_name"] = dataset_info.get("name")

        # Add metrics and answers
        exp_df = calculate_metrics_columns(exp, exp_df)

        all_rows.append(exp_df)

    if not all_rows:
        return pd.DataFrame()

    return pd.concat(all_rows, ignore_index=True)


def generate_readme_content(expset, full_experiments):
    md_content = []

    # Frontmatter
    md_content.append("---")
    md_content.append(f"pretty_name: {expset.get('name')}")
    md_content.append("tags:\n- evalap\n- evaluation\n- llm")
    md_content.append("---")

    md_content.append(f"# Experiment Set: {expset.get('name')} (ID: {expset.get('id')})\n")

    if expset.get("readme"):
        md_content.append(f"{expset.get('readme')}\n")

    # Generate Scores Table (reusing logic from reference script simplified)
    experiments_by_dataset = {}
    for exp in full_experiments:
        dataset_name = exp.get("dataset", {}).get("name", "Unknown Dataset")
        if dataset_name not in experiments_by_dataset:
            experiments_by_dataset[dataset_name] = []
        experiments_by_dataset[dataset_name].append(exp)

    for dataset_name, dataset_experiments in experiments_by_dataset.items():
        md_content.append(f"## Dataset: {dataset_name}\n")

        rows = []
        for exp in dataset_experiments:
            row = {}
            model_info = exp.get("model") or {}
            row["model"] = model_info.get("aliased_name") or model_info.get("name", "Unknown")

            for result in exp.get("results", []):
                metric_name = result.get("metric_aliased_name") or result.get("metric_name")
                scores = [x["score"] for x in result.get("observation_table", []) if pd.notna(x.get("score"))]
                if scores:
                    row[metric_name] = np.mean(scores)

            rows.append(row)

        if rows:
            df = pd.DataFrame(rows)
            # Reorder columns to put model first
            cols = ["model"] + [c for c in df.columns if c != "model"]
            df = df[cols]
            md_content.append(df.to_markdown(index=False))
            md_content.append("\n")

    return "\n".join(md_content)


def main():
    parser = argparse.ArgumentParser(description="Publish EvalAP Experiment Sets to Hugging Face")
    parser.add_argument("--id", type=int, help="Specific Experiment Set ID")
    parser.add_argument("--repo-id", required=True, help="Hugging Face Dataset Repo ID (e.g. user/dataset)")
    parser.add_argument("--dry-run", action="store_true", help="Generate files locally without uploading")
    parser.add_argument("--export-dir", default="export", help="Local directory for temporary files")
    args = parser.parse_args()

    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        # Try to find token in ~/.cache/huggingface/token or HF_TOKEN
        # If not dry run and we need to upload, warn
        pass  # hf_hub handles login checks usually, or we fail later

    api = HfApi(token=hf_token)

    # Create Repo if not exists (and not dry run)
    if not args.dry_run:
        try:
            create_repo(args.repo_id, repo_type="dataset", exist_ok=True, token=hf_token)
            logger.info(f"Ensured repo {args.repo_id} exists.")
        except Exception as e:
            logger.error(f"Error creating/accessing repo: {e}")
            return

    experiment_sets = []
    if args.id:
        experiment_sets = [{"id": args.id}]
    else:
        # Fetch all sets logic here if needed, keeping it simple for now as requested
        # The user request sample implies potentially one or all.
        logger.info("Fetching all experiment sets...")
        all_sets = fetch_json("/v1/experiment_sets", params={"limit": 1000, "backward": "false"})
        if all_sets:
            experiment_sets = all_sets

    for expset_stub in tqdm(experiment_sets, desc="Processing Sets"):
        expset_id = expset_stub["id"]
        logger.info(f"Processing Set {expset_id}...")

        expset = fetch_experiment_set_details(expset_id)
        if not expset:
            continue

        full_experiments = fetch_experiments_with_details(expset_id)
        if not full_experiments:
            logger.warning(f"No experiments found for set {expset_id}")
            continue

        # Prepare Directory
        set_dir_name = f"experiment_set_{expset_id}"
        local_set_path = Path(args.export_dir) / set_dir_name
        if local_set_path.exists():
            shutil.rmtree(local_set_path)
        local_set_path.mkdir(parents=True, exist_ok=True)

        # 1. Generate Parquet
        logger.info(f"Generating Parquet for set {expset_id}...")
        df_raw = prepare_raw_data(full_experiments)
        if not df_raw.empty:
            df_raw.to_parquet(local_set_path / "data.parquet", index=False)
        else:
            logger.warning(f"No raw data generated for set {expset_id}")

        # 2. Generate README.md
        readme_content = generate_readme_content(expset, full_experiments)
        with open(local_set_path / "README.md", "w") as f:
            f.write(readme_content)

        # 3. Generate individual experiment Markdowns (for browsability)
        logger.info(f"Generating details markdown for set {expset_id}...")
        details_dir = local_set_path / "details"
        details_dir.mkdir(exist_ok=True)

        # Create index content with links
        index_content = ["# details by Experiment\n"]

        sorted_experiments = sorted(full_experiments, key=lambda x: x.get("id", 0))
        for exp in sorted_experiments:
            exp_id = exp.get("id")
            exp_name = exp.get("name", str(exp_id))

            # Add link to index
            index_content.append(f"- [Experiment {exp_id}](details/experiment_{exp_id}.md) - {exp_name}")

            # Generate individual exp file
            exp_md = generate_experiment_markdown(
                exp, datasets_cache={}
            )  # Using local cache if possible or separate
            with open(details_dir / f"experiment_{exp_id}.md", "w") as f:
                f.write(exp_md)

        # Append index to README or save as separate index?
        # User request was "include metadata present in streamlit UI".
        # Streamlit has a "Details by Experiment" tab.
        # Let's append the list of experiments to the main README as well for easier navigation on HF.
        with open(local_set_path / "README.md", "a") as f:
            f.write("\n\n" + "\n".join(index_content))

        # 3. Upload to HF
        if not args.dry_run:
            logger.info(f"Uploading set {expset_id} to HF...")
            try:
                # Upload the folder content to a subdirectory in the dataset
                api.upload_folder(
                    folder_path=str(local_set_path),
                    repo_id=args.repo_id,
                    repo_type="dataset",
                    path_in_repo=set_dir_name,
                    commit_message=f"Add experiment set {expset_id}",
                )
            except Exception as e:
                logger.error(f"Failed to upload set {expset_id}: {e}")

    # After processing all sets, update the root README (index)
    if not args.dry_run:
        logger.info("Updating root README index...")
        try:
            update_repository_index(api, args.repo_id)
        except Exception as e:
            logger.error(f"Failed to update root index: {e}")

    logger.info("Done.")


def update_repository_index(api, repo_id):
    """
    Scans the repository for experiment sets and generates a root README.md
    listing them.
    """
    try:
        files = api.list_repo_files(repo_id=repo_id, repo_type="dataset")
    except Exception as e:
        logger.warning(f"Could listed repo files to generate index: {e}")
        return

    # Find experiment sets (look for experiment_set_*/README.md)
    set_ids = []
    for f in files:
        if f.startswith("experiment_set_") and f.endswith("/README.md"):
            # Extract ID from "experiment_set_{ID}/README.md"
            parts = f.split("/")
            if len(parts) >= 2:
                dirname = parts[0]
                if dirname.startswith("experiment_set_"):
                    try:
                        sid = int(dirname.replace("experiment_set_", ""))
                        set_ids.append(sid)
                    except ValueError:
                        pass

    set_ids = sorted(list(set(set_ids)))

    if not set_ids:
        logger.info("No experiment sets found in repo to index.")
        return

    # Generate README content
    lines = []
    lines.append("---")
    lines.append("tags:")
    lines.append("- evalap")
    lines.append("- evaluation")
    lines.append("- llm")
    lines.append("---")
    lines.append("# EvalAP Experiment Sets")
    lines.append("")
    lines.append("This repository contains experiment sets exported from EvalAP.")
    lines.append("")
    lines.append("## Available Sets")
    lines.append("")

    for sid in set_ids:
        lines.append(f"- [Experiment Set {sid}](./experiment_set_{sid}/README.md)")

    lines.append("")
    content = "\n".join(lines)

    # Upload README.md
    api.upload_file(
        path_or_fileobj=content.encode("utf-8"),
        path_in_repo="README.md",
        repo_id=repo_id,
        repo_type="dataset",
        commit_message="Update repository index",
    )
    logger.info("Root README index updated.")


if __name__ == "__main__":
    main()
