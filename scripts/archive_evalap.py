import argparse
import os
import re
from collections import defaultdict

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


def compute_failure_rates(experiments: list) -> tuple[dict, dict]:
    """Compute failure rates per model and metric."""
    model_stats = defaultdict(lambda: {"num_try": 0, "num_success": 0})
    metric_stats = defaultdict(lambda: {"num_try": 0, "num_success": 0})

    for experiment in experiments:
        model = experiment.get("model", {})
        model_name = model.get("name") if model else "Unknown"
        num_try = experiment.get("num_try", 0)
        num_success = experiment.get("num_success", 0)

        if model_name:
            model_stats[model_name]["num_try"] += num_try
            model_stats[model_name]["num_success"] += num_success

        for result in experiment.get("results", []):
            metric_name = result.get("metric_name")
            r_num_try = result.get("num_try", 0)
            r_num_success = result.get("num_success", 0)
            if metric_name:
                metric_stats[metric_name]["num_try"] += r_num_try
                metric_stats[metric_name]["num_success"] += r_num_success

    model_failure_rate = {
        name: 1 - (stats["num_success"] / stats["num_try"]) if stats["num_try"] > 0 else 0.0
        for name, stats in model_stats.items()
    }
    metric_failure_rate = {
        name: 1 - (stats["num_success"] / stats["num_try"]) if stats["num_try"] > 0 else 0.0
        for name, stats in metric_stats.items()
    }

    return model_failure_rate, metric_failure_rate


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

    # Dataset Info (from first experiment)
    if full_experiments:
        first_exp = full_experiments[0]
        ds_name = first_exp["dataset"].get("name", "Unknown")
        ds_size = first_exp["dataset"].get("size", "Unknown")
        md_content.append(f"**Dataset**: {ds_name} (Size: {ds_size})\n")

        # Judge Model
        judge = first_exp.get("judge_model")
        judge_name = judge.get("name") if judge else "No judge found"
        md_content.append(f"**Judge model**: {judge_name}\n")

    # Score Description
    score_desc = "**Score**: Averaged score on experiments metrics"
    if check_repeat_mode(full_experiments):
        score_desc += " *(aggregated on model repetition)*"
    md_content.append(f"{score_desc}\n")

    # Aggregate metrics
    data = []
    all_metrics = set()

    for exp in full_experiments:
        row = {
            "Model": (exp.get("model") or {}).get("name", "Unknown"),
            "Experiment": exp.get("name", str(exp.get("id"))),
        }

        # Add metrics
        results = exp.get("results", [])
        if results:
            for res in results:
                metric_name = res.get("metric_name")
                # Try to get numeric score first, check how it's stored
                # The API spec says 'observation_table' contains 'score'.
                # Usually we want the average score or the final score.
                # Assuming 'num_success' and some aggregation?
                # Let's look at how the UI does it. The UI likely averages the scores in observation_table.
                # For now, let's try to extract a representative score if possible, or just mark as Present.
                # Actually, in 'Result' schema there is NO direct average score field.
                # We need to compute it from 'observation_table' entries?
                # Iterate observations and average 'score'

                obs_table = res.get("observation_table", [])
                scores = [
                    o.get("score")
                    for o in obs_table
                    if o.get("score") is not None and isinstance(o.get("score"), (int, float))
                ]

                if scores:
                    avg_score = sum(scores) / len(scores)
                    row[metric_name] = round(avg_score, 4)
                    all_metrics.add(metric_name)
                else:
                    # Maybe it's a pass/fail or text?
                    row[metric_name] = "N/A"  # or check status
                    all_metrics.add(metric_name)

        data.append(row)

    if data:
        df = pd.DataFrame(data)
        # Ensure all metric columns exist (fill NaN)
        for m in all_metrics:
            if m not in df.columns:
                df[m] = None

        # Sort columns: Model, Experiment, then Metrics sorted alphabetically
        cols = ["Model", "Experiment"] + sorted(list(all_metrics))
        df = df[cols]

        md_content.append(df.to_markdown(index=False))
    else:
        md_content.append("No score data available.")

    md_content.append("\n")

    # 5. Set Overview Tab (Section 2)
    md_content.append("## Set Overview\n")
    # Simple table of experiments
    overview_data = []
    for exp in full_experiments:
        overview_data.append(
            {
                "ID": exp.get("id"),
                "Name": exp.get("name"),
                "Model": (exp.get("model") or {}).get("name"),
                "Status": exp.get("experiment_status"),
                "Created At": exp.get("created_at"),
            }
        )

    if overview_data:
        df_overview = pd.DataFrame(overview_data)
        md_content.append(df_overview.to_markdown(index=False))
    else:
        md_content.append("No overview data.")
    md_content.append("\n")

    # 6. Details by Experiment (Section 3) - The "Iterating Dropdown" equivalent
    md_content.append("## Details by Experiment\n")

    # Cache for datasets (id -> DataFrame)
    datasets_cache = {}

    for exp in full_experiments:
        model_name = (exp.get("model") or {}).get("name", "Unknown")
        exp_name = exp.get("name", str(exp.get("id")))

        md_content.append(f"### {model_name} - {exp_name}\n")

        results = exp.get("results", [])
        answers = exp.get("answers", [])

        # Determine Dataset ID and Fetch if needed
        dataset_info = exp.get("dataset", {})
        dataset_id = dataset_info.get("id")

        df_dataset = None
        if dataset_id:
            if dataset_id not in datasets_cache:
                print(f"Fetching dataset {dataset_id} content...")
                ds_full = fetch_json(f"/v1/dataset/{dataset_id}", params={"with_df": "true"})
                if ds_full and ds_full.get("df"):
                    try:
                        # df is a JSON string, need to parse it
                        datasets_cache[dataset_id] = pd.read_json(ds_full["df"])
                    except Exception as e:
                        print(f"Error parsing dataset {dataset_id} dataframe: {e}")
                        datasets_cache[dataset_id] = None
                else:
                    datasets_cache[dataset_id] = None

            df_dataset = datasets_cache[dataset_id]

        # Extract Q&A Data
        prompt = "N/A"
        expected_output = "N/A"
        actual_answer = "N/A"

        # Use the first answer to find the row index (num_line)
        if answers:
            first_ans = answers[0]
            actual_answer = first_ans.get("answer", "N/A")
            num_line = first_ans.get("num_line")

            if df_dataset is not None and num_line is not None and num_line < len(df_dataset):
                row = df_dataset.iloc[num_line]

                # Heuristics for columns
                # Try 'query', 'input', 'prompt', 'instruction' for input
                for col in ["query", "input", "prompt", "question", "instruction"]:
                    if col in row:
                        prompt = row[col]
                        break

                # Try 'output_true', 'expected_output', 'answer_true', 'gold' for expected
                for col in ["output_true", "expected_output", "answer", "output", "gold", "ground_truth"]:
                    if col in row:
                        expected_output = row[col]
                        break

        def format_blockquote(text):
            if not isinstance(text, str):
                text = str(text) if text is not None else "N/A"
            return "\n> ".join(text.split("\n"))

        md_content.append(f"**Prompt**:\n\n> {format_blockquote(prompt)}\n\n")
        md_content.append(f"**Answer**:\n\n> {format_blockquote(actual_answer)}\n\n")
        md_content.append(f"**Expected Output**:\n\n> {format_blockquote(expected_output)}\n\n")

        # Metrics Table
        if results:
            for res in results:
                metric_name = res.get("metric_name")
                md_content.append(f"#### Metric: {metric_name}\n")

                obs_table = res.get("observation_table", [])
                if obs_table:
                    # Create a DataFrame for the observations
                    obs_data = []
                    for o in obs_table:
                        # Try to flatten the observation object if it's a dict
                        obs_content = o.get("observation")
                        score = o.get("score")
                        error = o.get("error_msg")

                        row_d = {"Score": score, "Error": error}
                        if isinstance(obs_content, dict):
                            for k, v in obs_content.items():
                                row_d[f"Obs_{k}"] = str(v)[:200]  # Truncate for sanity
                        else:
                            row_d["Observation"] = str(obs_content)[:200]

                        obs_data.append(row_d)

                    if obs_data:
                        df_obs = pd.DataFrame(obs_data)
                        md_content.append(df_obs.to_markdown(index=False))
                    else:
                        md_content.append("No observations found.")
                md_content.append("\n")
        else:
            md_content.append("No results found.\n")

    # 7. Global Infos (Section 4)
    md_content.append("## Global Infos\n")
    # Aggregated stats
    total_exp = len(full_experiments)
    finished_exp = sum(1 for e in full_experiments if e.get("experiment_status") == "finished")

    md_content.append(f"- **Total Experiments**: {total_exp}")
    md_content.append(f"- **Finished**: {finished_exp}")
    md_content.append(f"- **Failed/Other**: {total_exp - finished_exp}")

    # Eco stats if available
    # Only if `with_eco=True` returned meaningful data in `dataset` or `experiment` object?
    # Or maybe we sum up execution times?
    # Or maybe we sum up execution times?
    total_duration = sum((e.get("execution_time") or 0) for e in full_experiments)
    md_content.append(f"- **Total Execution Time**: {total_duration}s")
    md_content.append("\n")

    # Failure Rate Analysis
    md_content.append("### Failure Rate Analysis\n")
    model_failure, metric_failure = compute_failure_rates(full_experiments)

    md_content.append("#### By Model\n")
    if not model_failure or all(v == 0 for v in model_failure.values()):
        md_content.append("No models with failure.\n")
    else:
        for model, rate in sorted(model_failure.items(), key=lambda x: -x[1]):
            md_content.append(f"- **{model}**: {rate:.1%} failures")

    md_content.append("\n#### By Metric\n")
    if not metric_failure or all(v == 0 for v in metric_failure.values()):
        md_content.append("No metrics with failure.\n")
    else:
        for metric, rate in sorted(metric_failure.items(), key=lambda x: -x[1]):
            md_content.append(f"- **{metric}**: {rate:.1%} failures")

    md_content.append("\n")

    # Save file
    filename = f"experiment_set_{experiment_set_id}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        f.write("\n".join(md_content))

    print(f"Saved archive to {filepath}")


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
