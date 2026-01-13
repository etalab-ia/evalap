import argparse
import os
import re
from io import StringIO

import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

API_BASE_URL = "https://evalap.etalab.gouv.fr"


def fetch_json(endpoint, params=None):
    url = f"{API_BASE_URL}{endpoint}"
    headers = {"User-Agent": "EvalAP-Archiver/1.0", "Accept": "application/json"}
    token = os.getenv("EVALAP_API_KEY")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        response = getattr(e, "response", None)
        if response is not None:
            print(f"Response: {response.text}")
        return None


def check_repeat_mode(experiments: list) -> bool:
    """Check whether the experiment is related to a repetition."""
    for expe in experiments:
        name = expe.get("name", "")
        if re.search(r"__\d+$", name):
            return True
    return False


def quote_markdown(text):
    """Prefixes each line of text with '> ' for blockquoting multi-line values."""
    if not text:
        return "> "
    return "> " + "\n> ".join(str(text).splitlines())


def generate_markdown(experiment_set_id, output_dir):
    print(f"Processing Experiment Set ID: {experiment_set_id}")

    # 1. Fetch Experiment Set Details
    expset = fetch_json(f"/v1/experiment_set/{experiment_set_id}")
    if not expset:
        print(f"Skipping set {experiment_set_id} due to fetch error.")
        return

    # 2. Fetch Experiments
    # Note: endpoints.py has orphan=True by default, which seems to exclude experiments in a set?
    # verified via curl that orphan=false is needed.
    experiments = fetch_json(
        "/v1/experiments", params={"set_id": experiment_set_id, "limit": 1000, "orphan": "false"}
    )
    if not experiments:
        print(f"No experiments found for set {experiment_set_id}.")
        return

    # 3. Fetch Full Details for each experiment (with results, answers, eco)
    full_experiments = []
    print(f"Fetching details for {len(experiments)} experiments...")
    for exp in tqdm(experiments, desc="Fetching Experiments"):
        full_exp = fetch_json(
            f"/v1/experiment/{exp['id']}",
            params={"with_results": "true", "with_answers": "true", "with_eco": "true"},
        )
        if full_exp:
            full_experiments.append(full_exp)

    # --- Generate Content ---

    md_content = []

    # Frontmatter
    md_content.append("---")
    md_content.append(f"id: {expset.get('id')}")
    md_content.append(f'name: "{expset.get("name")}"')
    md_content.append(f"date: {expset.get('created_at')}")
    md_content.append(f'description: "{expset.get("description", "")}"')
    md_content.append("tags: []")  # Placeholder as tags aren't clear in API yet
    md_content.append("---\n")

    # Calculate Finished %
    total_obs_success = sum(e.get("num_observation_success", 0) for e in full_experiments)

    # Estimate total expected observations (dataset size * num_metrics)
    # This might be more accurate if we assume dataset size is constant or sum it up
    observation_length = sum(e["dataset"].get("size", 0) * e.get("num_metrics", 0) for e in full_experiments)

    finished_ratio = 0
    if observation_length > 0:
        finished_ratio = min(100, int(total_obs_success / observation_length * 100))

    md_content.append(f"# Experiment Set: {expset.get('name')} (ID: {expset.get('id')})\n")

    if expset.get("readme"):
        md_content.append(f"{expset.get('readme')}\n")

    md_content.append(f"**Finished**: {finished_ratio}%\n")

    # 4. Scores Tab (Section 1)
    md_content.append("## Scores\n")

    # Group experiments by dataset (same as Streamlit UI)
    experiments_by_dataset = {}
    for exp in full_experiments:
        dataset_name = exp.get("dataset", {}).get("name", "Unknown Dataset")
        if dataset_name not in experiments_by_dataset:
            experiments_by_dataset[dataset_name] = []
        experiments_by_dataset[dataset_name].append(exp)

    # Process each dataset group
    for dataset_name, dataset_experiments in experiments_by_dataset.items():
        # Dataset Info
        ds_size = dataset_experiments[0]["dataset"].get("size", "Unknown")
        md_content.append(f"**Dataset**: {dataset_name} (Size: {ds_size})\n")

        # Judge Model (from first experiment in this dataset group)
        available_judges = sorted(
            list(set(exp["judge_model"]["name"] for exp in dataset_experiments if exp.get("judge_model")))
        ) or ["No judge found"]
        md_content.append(f"**Judge model**: {available_judges[0]}\n")

        # Score Description
        is_repeat_mode = check_repeat_mode(dataset_experiments)
        score_desc = "**Score**: Averaged score on experiments metrics"
        if is_repeat_mode:
            score_desc += " *(aggregated on model repetition)*"
        md_content.append(f"{score_desc}\n")

        # Build rows for this dataset group (like Streamlit display_experiment_set_score)
        rows = []
        rows_support = []  # Track support (number of items per metric)
        for exp in dataset_experiments:
            row = {}
            row_support = {}

            # Determine model name (similar to Streamlit logic)
            if exp.get("model"):
                model_name = exp["model"].get("aliased_name") or exp["model"].get("name", "Unknown")
            else:
                model_name = f"Undefined model ({exp.get('name', 'Unknown')})"
            row["model"] = model_name
            row_support["model"] = model_name

            # Aggregate results/scores (like Streamlit)
            for result in exp.get("results", []):
                metric_name = result.get("metric_aliased_name") or result.get("metric_name")
                scores = [x["score"] for x in result.get("observation_table", []) if pd.notna(x.get("score"))]
                if scores:
                    row[metric_name] = np.mean(scores)
                    row_support[f"{metric_name}_support"] = len(scores)

            rows.append(row)
            rows_support.append(row_support)

        if not rows:
            md_content.append("No valid experiment results found.\n\n")
            continue

        df = pd.DataFrame(rows)
        df_support = pd.DataFrame(rows_support)

        # Check if there's support variation (like Streamlit _check_support_variation)
        def check_support_variation(df_sup):
            metric_cols = [col for col in df_sup.columns if col != "model"]
            for col in metric_cols:
                if df_sup[col].nunique(dropna=True) > 1:
                    return True
            return False

        has_support_variation = check_support_variation(df_support)

        # Reorder columns: model first, then metrics sorted alphabetically
        metric_columns = [col for col in df.columns if col != "model"]
        new_column_order = ["model"] + sorted(metric_columns)
        df = df[[col for col in new_column_order if col in df.columns]]

        # Reorder support columns similarly
        support_columns = [col for col in df_support.columns if col != "model"]
        support_column_order = ["model"] + sorted(support_columns)
        df_support = df_support[[col for col in support_column_order if col in df_support.columns]]

        # Apply aggregation when in repeat mode (like Streamlit _format_experiments_score_df)
        if is_repeat_mode and "model" in df.columns and df["model"].notna().all():
            # Strip repetition trailing code from model names
            df["model"] = df["model"].str.replace(r"__\d+$", "", regex=True)
            df_support["model"] = df_support["model"].str.replace(r"__\d+$", "", regex=True)

            # Group by model and calculate mean and std for all numeric columns
            grouped = df.groupby("model").agg(["mean", "std"]).reset_index()
            grouped_support = df_support.groupby("model").agg(["mean", "std"]).reset_index()

            # Create a new DataFrame to store the formatted results
            result_df = pd.DataFrame()
            result_df["model"] = grouped["model"]

            # Format each metric column as "mean ± std"
            for column in df.columns:
                if column != "model":
                    decimals = 4 if "_consumption" in column else 2
                    mean_vals = grouped[(column, "mean")].round(decimals).astype(str)
                    std_vals = grouped[(column, "std")].round(decimals).astype(str)

                    # Only add ± std if there's actual variation
                    if all(
                        x is None or x == 0 or (isinstance(x, float) and np.isnan(x))
                        for x in grouped[(column, "std")]
                    ):
                        result_df[column] = mean_vals
                    else:
                        result_df[column] = mean_vals + " ± " + std_vals

            df = result_df

            # Format support DataFrame similarly
            result_support_df = pd.DataFrame()
            result_support_df["model"] = grouped_support["model"]

            for column in df_support.columns:
                if column != "model":
                    decimals = 2
                    mean_vals = grouped_support[(column, "mean")].round(decimals).astype(str)
                    std_vals = grouped_support[(column, "std")].round(decimals).astype(str)

                    # Only add ± std if there's actual variation
                    if all(
                        x is None or x == 0 or (isinstance(x, float) and np.isnan(x))
                        for x in grouped_support[(column, "std")]
                    ):
                        result_support_df[column] = mean_vals
                    else:
                        result_support_df[column] = mean_vals + " ± " + std_vals

            df_support = result_support_df

        # Sort by a sensible default metric if available
        sort_metric = None
        preferred_metrics = [
            "judge_precision",
            "judge_notator",
            "answer_relevancy",
            "judge_exactness",
        ]
        for metric in preferred_metrics:
            if metric in df.columns:
                sort_metric = metric
                break

        if sort_metric is None and len(df.columns) > 1:
            sort_metric = [col for col in df.columns if col != "model"][0]

        if sort_metric:

            def extract_mean(value):
                try:
                    return float(str(value).split("±")[0].strip())
                except (ValueError, TypeError):
                    return value

            # Get the sorted order from df
            df = df.sort_values(
                by=sort_metric,
                key=lambda x: x.map(extract_mean),
                ascending=False,
            )

            # Apply same order to df_support
            if "model" in df_support.columns:
                df_support = df_support.set_index("model").loc[df["model"].values].reset_index()

        md_content.append(df.to_markdown(index=False))
        md_content.append("\n")

        # Add Support table if there's variation (like Streamlit)
        if has_support_variation:
            support_desc = (
                f"**Support**: the numbers of item on which the metrics "
                f"is computed (total items = {ds_size})\n"
            )
            md_content.append(support_desc)
            md_content.append(df_support.to_markdown(index=False))
            md_content.append("\n")

    md_content.append("")

    # 5. Set Overview Tab (Section 2)
    md_content.append("## Set Overview\n")

    # Helper function to format model params (like Streamlit _format_model_params)
    def format_model_params(exp):
        if not exp.get("model"):
            return None
        model = exp["model"]
        model_params = (model.get("sampling_params") or {}) | (model.get("extra_params") or {})
        if model.get("system_prompt"):
            # Hash system prompt to a short string
            import hashlib

            sys_hash = hashlib.md5(model["system_prompt"].encode()).hexdigest()[:4]
            model_params["sys_prompt"] = sys_hash
        return model_params if model_params else None

    # Build table of experiments
    overview_data = []
    for exp in full_experiments:
        # Use aliased_name if available, else name
        model = exp.get("model") or {}
        model_name = model.get("aliased_name") or model.get("name", "")

        # Dataset name
        dataset = exp.get("dataset") or {}
        dataset_name = dataset.get("name", "")

        # Model params
        model_params = format_model_params(exp)
        model_params_str = str(model_params) if model_params else "{}"

        overview_data.append(
            {
                "Id": exp.get("id"),
                "Name": exp.get("name"),
                "Dataset": dataset_name,
                "Model": model_name,
                "Model params": model_params_str,
                "Status": exp.get("experiment_status"),
                "Created at": exp.get("created_at"),
                "Num try": exp.get("num_try"),
                "Num success": exp.get("num_success"),
            }
        )

    if overview_data:
        df_overview = pd.DataFrame(overview_data)
        # Sort by Id ascending (like Streamlit)
        df_overview = df_overview.sort_values(by="Id", ascending=True)
        md_content.append(df_overview.to_markdown(index=False))
    else:
        md_content.append("No overview data.")
    md_content.append("\n")

    # 6. Details by Experiment links in Index
    index_content = list(md_content)  # Copy current content for index
    index_content.append("## Details by Experiment\n")

    # 7. Prepare directories
    set_dir = os.path.join(output_dir, f"experiment_set_{experiment_set_id}")
    details_dir = os.path.join(set_dir, "details")
    os.makedirs(details_dir, exist_ok=True)

    # Cache for datasets (id -> DataFrame)
    datasets_cache = {}

    # Sort experiments by ID ascending (like Streamlit)
    sorted_experiments = sorted(full_experiments, key=lambda x: x.get("id", 0))

    for exp in sorted_experiments:
        exp_id = exp.get("id")
        exp_name = exp.get("name", str(exp_id))
        exp_readme = exp.get("readme")

        # Add link to index
        index_content.append(f"- [Experiment {exp_id}](details/experiment_{exp_id}.md) - {exp_name}")

        # Start individual experiment markdown
        exp_md = []
        exp_md.append(f"# Experiment {exp_id}\n")
        exp_md.append("[← Back to Index](../index.md)\n")

        # Dataset info
        dataset_info = exp.get("dataset", {})
        dataset_name = dataset_info.get("name", "Unknown")
        dataset_id = dataset_info.get("id")

        # Judge model
        judge_model = exp.get("judge_model")
        judge_model_name = judge_model.get("name") if judge_model else "None"

        # Model info
        model = exp.get("model") or {}

        exp_md.append(f"**Name:** {exp_name}\n")
        exp_md.append(f"**Readme:** {exp_readme}\n")
        exp_md.append(f"**Dataset:** {dataset_name}\n")
        exp_md.append(f"**Judge model:** {judge_model_name}\n")
        exp_md.append(f"**Model:** {model}\n")
        exp_md.append("## Data Table\n")

        # Fetch dataset content if not cached
        df = None
        if dataset_id:
            if dataset_id not in datasets_cache:
                ds_full = fetch_json(f"/v1/dataset/{dataset_id}", params={"with_df": "true"})
                if ds_full and ds_full.get("df"):
                    try:
                        datasets_cache[dataset_id] = pd.read_json(StringIO(ds_full["df"]))
                    except Exception as e:
                        print(f"Error parsing dataset {dataset_id} dataframe: {e}")
                        datasets_cache[dataset_id] = None
                else:
                    datasets_cache[dataset_id] = None

            if datasets_cache.get(dataset_id) is not None:
                df = datasets_cache[dataset_id].copy()

        if df is None:
            exp_md.append("No dataset content available.\n\n")
        else:
            # Apply sample if present
            sample = exp.get("sample")
            if sample:
                df = df.iloc[sample]

            # Merge answers
            answers = exp.get("answers", [])
            if answers:
                answer_fields_to_show = ["answer", "error_msg", "context", "retrieval_context"]
                for field in answer_fields_to_show:
                    values = {answer["num_line"]: answer.get(field) for answer in answers}
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
                        obs["num_line"]: obs["score"] for obs in result.get("observation_table", [])
                    }
                    df[f"result_{metric_name}"] = df.index.map(observations)

            # Reorder columns
            if not df.empty:
                result_cols = sorted([col for col in df.columns if col.startswith("result_")])
                other_cols = [col for col in df.columns if not col.startswith("result_")]
                df = df[other_cols + result_cols]

            # Truncate long text columns
            for col in df.columns:
                if df[col].dtype == "object":
                    df[col] = df[col].apply(
                        lambda x: str(x)[:100] + "..." if isinstance(x, str) and len(str(x)) > 100 else x
                    )

            exp_md.append(df.to_markdown())
            exp_md.append("\n\n")

        # Save individual experiment file
        exp_filename = f"experiment_{exp_id}.md"
        exp_filepath = os.path.join(details_dir, exp_filename)
        with open(exp_filepath, "w") as f:
            f.write("\n".join(exp_md))

    # 8. Save index file
    index_path = os.path.join(set_dir, "index.md")
    with open(index_path, "w") as f:
        f.write("\n".join(index_content))

    print(f"Saved archive to {set_dir}")


def main():
    parser = argparse.ArgumentParser(description="Archive EvalAP Experiment Sets to Markdown")
    parser.add_argument("--id", type=int, help="Specific Experiment Set ID to archive")
    parser.add_argument("--output-dir", default="archives", help="Directory to save markdown files")

    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    if args.id:
        experiment_sets = [{"id": args.id}]
    else:
        print("Fetching all experiment sets...")
        # Get all sets
        response = fetch_json("/v1/experiment_sets", params={"limit": 1000, "backward": "false"})
        if not response:
            print("Failed to fetch experiment sets.")
            return
        experiment_sets = response

    print(f"Found {len(experiment_sets)} experiment sets to process.")

    for expset in tqdm(experiment_sets, desc="Processing Sets"):
        try:
            generate_markdown(expset["id"], args.output_dir)
        except Exception as e:
            print(f"Failed to process set {expset['id']}: {e}")
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    main()
