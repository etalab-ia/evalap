import argparse
import logging
import os
import re
import shutil
import time
from io import StringIO
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv
from huggingface_hub import HfApi, create_repo
from tqdm import tqdm

load_dotenv()

API_BASE_URL = "https://evalap.etalab.gouv.fr"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    # Normalize unicode characters
    import unicodedata

    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    # Convert to lowercase and replace spaces/special chars with hyphens
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[-\s]+", "-", text).strip("-")
    return text


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


def prepare_experiment_data(exp, datasets_cache):
    """Prepare data for a single experiment."""
    dataset_info = exp.get("dataset")
    if not dataset_info or not dataset_info.get("id"):
        return pd.DataFrame()

    dataset_id = dataset_info["id"]
    base_df = get_dataset_dataframe(dataset_id, datasets_cache)
    if base_df is None:
        return pd.DataFrame()

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

    return exp_df


def generate_experiment_set_readme(expset, full_experiments):
    """Generate README content for a single experiment set repository."""
    md_content = []

    # Build configs for each experiment (using experiment name as config)
    exp_configs = []
    for exp in full_experiments:
        exp_id = exp.get("id")
        exp_name = exp.get("name", str(exp_id))
        config_name = slugify(f"{exp_name}-{exp_id}")
        exp_configs.append({"id": exp_id, "name": exp_name, "config_name": config_name})

    # Frontmatter with configs
    md_content.append("---")
    md_content.append(f"pretty_name: {expset.get('name')}")

    if exp_configs:
        md_content.append("configs:")
        for i, cfg in enumerate(exp_configs):
            md_content.append(f"  - config_name: {cfg['config_name']}")
            md_content.append(f"    data_files: data/{cfg['config_name']}/*.parquet")
            if i == 0:
                md_content.append("    default: true")

    md_content.append("tags:")
    md_content.append("  - evalap")
    md_content.append("  - evaluation")
    md_content.append("  - llm")
    md_content.append("---")
    md_content.append("")

    md_content.append(f"# {expset.get('name')} (ID: {expset.get('id')})\n")

    if expset.get("readme"):
        md_content.append(f"{expset.get('readme')}\n")

    # Overview section
    md_content.append("## Overview\n")
    md_content.append(f"This dataset contains **{len(full_experiments)} experiments** ")
    md_content.append("from the EvalAP evaluation platform.\n")

    # Collect unique datasets and models
    datasets_set = set()
    models_set = set()
    metrics_set = set()
    for exp in full_experiments:
        ds = exp.get("dataset", {}).get("name")
        if ds:
            datasets_set.add(ds)
        model = (exp.get("model") or {}).get("name")
        if model:
            models_set.add(model)
        for result in exp.get("results", []):
            metric = result.get("metric_aliased_name") or result.get("metric_name")
            if metric:
                metrics_set.add(metric)

    if datasets_set:
        md_content.append(f"**Datasets:** {', '.join(sorted(datasets_set))}\n")
    if models_set:
        md_content.append(f"**Models evaluated:** {', '.join(sorted(models_set))}\n")
    if metrics_set:
        md_content.append(f"**Metrics:** {', '.join(sorted(metrics_set))}\n")

    # Generate score tables per dataset
    md_content.append("\n## Scores\n")

    experiments_by_dataset = {}
    for exp in full_experiments:
        dataset_name = exp.get("dataset", {}).get("name", "Unknown Dataset")
        if dataset_name not in experiments_by_dataset:
            experiments_by_dataset[dataset_name] = []
        experiments_by_dataset[dataset_name].append(exp)

    import numpy as np

    for dataset_name, dataset_experiments in experiments_by_dataset.items():
        md_content.append(f"### {dataset_name}\n")

        # Build rows with mean ± std for each metric
        rows = []
        for exp in dataset_experiments:
            row = {}
            model_info = exp.get("model") or {}
            row["model"] = model_info.get("aliased_name") or model_info.get("name", "Unknown")

            for result in exp.get("results", []):
                metric_name = result.get("metric_aliased_name") or result.get("metric_name")
                scores = [
                    x["score"]
                    for x in result.get("observation_table", [])
                    if x.get("score") is not None and not np.isnan(x.get("score", float("nan")))
                ]
                if scores:
                    mean = np.mean(scores)
                    std = np.std(scores)
                    row[metric_name] = f"{mean:.2f} ± {std:.2f}"

            rows.append(row)

        if rows:
            import pandas as pd

            df = pd.DataFrame(rows)
            cols = ["model"] + [c for c in sorted(df.columns) if c != "model"]
            df = df[cols]
            md_content.append(df.to_markdown(index=False))
            md_content.append("\n")

    # Note about experiments
    md_content.append("\n## Usage\n")
    md_content.append("Use the dropdown above to select an experiment configuration.\n")

    return "\n".join(md_content), exp_configs


def main():
    parser = argparse.ArgumentParser(description="Publish EvalAP Experiment Sets to Hugging Face")
    parser.add_argument("--id", type=int, help="Specific Experiment Set ID")
    parser.add_argument("--org", required=True, help="Hugging Face Organization/User (e.g. etalab-ia)")
    parser.add_argument("--dry-run", action="store_true", help="Generate files locally without uploading")
    parser.add_argument("--export-dir", default="export", help="Local directory for temporary files")
    parser.add_argument(
        "--collection",
        default="evalap-experiments",
        help="HF Collection slug to add datasets to (default: evalap-experiments)",
    )
    args = parser.parse_args()

    hf_token = os.getenv("HF_TOKEN")
    api = HfApi(token=hf_token)

    experiment_sets = []
    if args.id:
        experiment_sets = [{"id": args.id}]
    else:
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

        # Generate slugified repo name from experiment set name and ID
        expset_name = expset.get("name", f"experiment-set-{expset_id}")
        repo_name = f"evalap-{slugify(expset_name)}-{expset_id}"
        repo_id = f"{args.org}/{repo_name}"

        logger.info(f"Repository: {repo_id}")

        # Prepare local directory
        local_path = Path(args.export_dir) / repo_name
        if local_path.exists():
            shutil.rmtree(local_path)
        local_path.mkdir(parents=True, exist_ok=True)

        # Generate README with configs for each experiment
        readme_content, exp_configs = generate_experiment_set_readme(expset, full_experiments)
        with open(local_path / "README.md", "w") as f:
            f.write(readme_content)

        # Generate parquet files for each experiment (as separate configs)
        datasets_cache = {}
        data_dir = local_path / "data"
        data_dir.mkdir(exist_ok=True)

        for exp, cfg in zip(full_experiments, exp_configs, strict=True):
            config_dir = data_dir / cfg["config_name"]
            config_dir.mkdir(exist_ok=True)

            df = prepare_experiment_data(exp, datasets_cache)
            if not df.empty:
                df.to_parquet(config_dir / "data.parquet", index=False)

        # Create repo and upload
        if not args.dry_run:
            try:
                create_repo(repo_id, repo_type="dataset", exist_ok=True, token=hf_token)
                logger.info(f"Ensured repo {repo_id} exists.")
            except Exception as e:
                logger.error(f"Error creating repo {repo_id}: {e}")
                continue

            logger.info(f"Uploading to {repo_id}...")
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    api.upload_folder(
                        folder_path=str(local_path),
                        repo_id=repo_id,
                        repo_type="dataset",
                        commit_message=f"Upload experiment set {expset_id}",
                    )
                    logger.info(f"Successfully uploaded {repo_id}")
                    break
                except Exception as e:
                    if "timed out" in str(e).lower() and attempt < max_retries - 1:
                        wait_time = 2 ** (attempt + 1)
                        logger.warning(f"Timeout, retrying in {wait_time}s... ({attempt + 1}/{max_retries})")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Failed to upload {repo_id}: {e}")
                        break

            # Add to collection
            add_to_collection(api, args.org, args.collection, repo_id)

    logger.info("Done.")


def add_to_collection(api, org, collection_slug, repo_id):
    """Add a dataset to a HuggingFace collection, creating it if needed."""
    collection_id = f"{org}/{collection_slug}"

    try:
        # Try to get existing collection
        collection = api.get_collection(collection_id)
        logger.info(f"Found existing collection: {collection_id}")
    except Exception:
        # Create collection if it doesn't exist
        try:
            collection = api.create_collection(
                title="EvalAP Experiments",
                namespace=org,
                description="Experiment sets exported from the EvalAP evaluation platform.",
                exists_ok=True,
            )
            logger.info(f"Created collection: {collection.slug}")
        except Exception as e:
            logger.warning(f"Could not create collection: {e}")
            return

    # Check if item already in collection
    existing_items = [item.item_id for item in collection.items]
    if repo_id in existing_items:
        logger.info(f"{repo_id} already in collection")
        return

    # Add item to collection
    try:
        api.add_collection_item(
            collection_slug=collection.slug,
            item_id=repo_id,
            item_type="dataset",
        )
        logger.info(f"Added {repo_id} to collection {collection.slug}")
    except Exception as e:
        logger.warning(f"Could not add {repo_id} to collection: {e}")


if __name__ == "__main__":
    main()
