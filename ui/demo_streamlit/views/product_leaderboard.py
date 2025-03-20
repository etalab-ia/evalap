from itertools import groupby
from operator import itemgetter
from pathlib import Path
import json
import re
from collections import defaultdict
from copy import deepcopy

import numpy as np
import pandas as pd
import streamlit as st
import yaml

from utils import fetch, calculate_tokens_per_second

DEFAULT_METRIC = "judge_exactness"

#TODO:
# recup list mtetric du produit et n'afficher que les résultats dessus 


def load_product_config() -> dict:
    """Load product configuration from YAML file."""
    try:
        config_path = Path("config") / "products" / "product_config.yml"
        
        if not config_path.exists():
            st.error(f"Configuration file not found at: {config_path}")
            return {"products": {}}

        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        st.error(f"Error loading configuration: {str(e)}")
        return {"products": {}}


def fetch_experiment_results(exp_id: int) -> dict:
    """Fetch results for a single experiment."""
    return fetch("get", f"/experiment/{exp_id}", {"with_dataset": "true"})


@st.cache_data(ttl=300)
def fetch_leaderboard(metric_name: str = DEFAULT_METRIC, dataset_name: str | None = None, limit: int = 10) -> dict:
    """Fetch leaderboard data with caching."""
    endpoint = "/leaderboard"
    params = {"metric_name": metric_name}
    if dataset_name:
        params["dataset_name"] = dataset_name
    return fetch("get", endpoint, params)


def fetch_datasets() -> list[dict]:
    return fetch("get", "/datasets")


def format_column_name(name: str) -> str:
    """Format column names for better readability."""
    return name.replace("_", " ").title()


def display_model_production(model_info: dict, default_metric: str) -> None:
    """Display production model information and metrics."""
    st.write("#### Production Model")
    current_model = model_info.get("current", {})
    st.write(
        f"Current Model: {current_model.get('name', 'N/A')} "
        f"(ID: {current_model.get('id', 'N/A')}) - "
        f"v{current_model.get('version', 'N/A')} - "
        f"Last updated: {current_model.get('last_updated', 'N/A')}"
    )

    exp_id = current_model.get("id")
    if not exp_id:
        return

    try:
        results = fetch_experiment_results(exp_id)
        if not results or "results" not in results:
            st.info(f"No results found for experiment {exp_id}")
            return

        metrics_data = {"Model": current_model.get("name", "N/A")}
        tokens, times = [], []

        for result in results["results"]:
            metric_name = result["metric_name"]
            scores = [obs["score"] for obs in result["observation_table"]]
            mean_score = sum(scores) / len(scores)

            if metric_name == "nb_tokens_completion":
                tokens = scores
            elif metric_name == "generation_time":
                times = scores
            else:
                column_name = f"{format_column_name(metric_name)} Score" if metric_name == default_metric else metric_name
                metrics_data[column_name] = round(mean_score, 2)

        if tokens and times:
            tokens_per_second = [
                calculate_tokens_per_second(t, tm) for t, tm in zip(tokens, times)
            ]
            tokens_per_second = [tps for tps in tokens_per_second if tps is not None]

            if tokens_per_second:
                metrics_data["tokens_per_second"] = round(
                    sum(tokens_per_second) / len(tokens_per_second), 2
                )

        df = pd.DataFrame([metrics_data])
        st.dataframe(df)

    except Exception as e:
        st.error(f"Error fetching results for experiment {exp_id}: {str(e)}")


def _all_equal(lst):
    return all(x == lst[0] for x in lst)


def _remove_commons_items(model_params: list[dict], first=True) -> list[dict]:
    if first:
        model_params = deepcopy(model_params)

    common_keys = set.intersection(*(set(d.keys()) for d in model_params))
    for k in common_keys:
        if _all_equal([d[k] for d in model_params]):
            _ = [d.pop(k) for d in model_params]
        elif all(isinstance(d[k], dict) for d in model_params):
            # improves: works with any instead of all
            # take all dict value (recurse)
            # reinsert dict value in same order
            x = [(i, d[k]) for i, d in enumerate(model_params) if isinstance(d[k], dict)]
            idx, params = zip(*x)
            params = _remove_commons_items(list(params), first=False)
            for i, _id in enumerate(idx):
                if not params[i]:
                    model_params[_id].pop(k)
                model_params[_id][k] = params[i]
        elif all(isinstance(d[k], list) for d in model_params):
            # @improves: works with any instead of all
            # take all dict value in  list value (recurse)
            # reinsert dict value in same order
            pass

    return model_params


def _rename_model_variants(experiments: list) -> list:
    """
    Inplace add a _name attribute to experiment several model name are equal to help
    distinguish them
    """
    names = [exp["model"]["name"] for exp in experiments if exp.get("model")]
    if len(set(names)) == len(names):
        return experiments

    names = []
    for i, exp in enumerate(experiments):
        if not exp.get("model"):
            continue

        name = exp["model"]["name"]
        _name = name
        suffix = ""
        if re.search(r"__\d+$", name):
            parts = name.rsplit("__", 1)
            _name = parts[0]
            suffix = parts[1]

        names.append(
            {
                "pos": i,
                "name": name,
                "_name": _name,
                "suffix": suffix,
            }
        )

    # Find the experiments that have an equal _model name
    model_names = defaultdict(list)
    for item in names:
        if not item:
            continue
        model_names[item["_name"]].append(item["pos"])

    # Canonize model names
    for _name, ids in model_names.items():
        if len(ids) <= 1:
            continue

        # List of model params
        model_params = [
            (experiments[i]["model"].get("sampling_params") or {})
            | (experiments[i]["model"].get("extra_params") or {})
            for i in ids
        ]

        # remove commons parameters
        model_diff_params = _remove_commons_items(model_params)

        for model in names:
            pos = next((x for x in ids if model["pos"] == x), None)
            if not pos:
                continue

            # Finally renamed it !
            variant = model_diff_params[ids.index(pos)]
            if variant:
                variant = json.dumps(variant)
                variant = variant.replace('"', "").replace(" ", "")

                experiments[pos]["_model"] = "#".join([_name, variant]) + model["suffix"]


def add_repeat_column(df: pd.DataFrame) -> pd.DataFrame:
    def check_repeat(name: str) -> bool:
        if pd.isna(name): 
            return False
        return bool(re.search(r"__\d+$", str(name)))
    
    df['repeat'] = df['Experiment name'].apply(check_repeat)
    return df


def process_leaderboard_data(
    leaderboard_data: dict,
    metric_name: str,
    metrics_list_for_decision,
    current_model_id: int | None = None,
) -> pd.DataFrame | None:

    experiments = []
    exp_mapping = {}
    for entry in leaderboard_data["entries"]:
        if current_model_id and entry["experiment_id"] == current_model_id:
            continue
            
        exp = {
            "model": {
                "name": entry["model_name"],
                "sampling_params": entry.get("sampling_param", {}),
                "extra_params": entry.get("extra_param", {})
            }
        }
        experiments.append(exp)
        exp_mapping[entry["experiment_id"]] = exp

    _rename_model_variants(experiments)

    entries = []
    for entry in leaderboard_data["entries"]:
        if current_model_id and entry["experiment_id"] == current_model_id:
            continue

        exp = exp_mapping.get(entry["experiment_id"], {})
        model_name = entry["model_name"]
        renamed_model = exp.get("_model", model_name)
        
        params = {**entry.get("sampling_param", {}), **entry.get("extra_param", {})}
        parameters = json.dumps(params) if params else ""
        
        processed_entry = {
            "Experiment ID": entry["experiment_id"],
            "Experiment name": entry["experiment_name"],
            "Model": model_name,
            "Model_renamed": renamed_model,
            "Parameters": parameters,
            "Created at": entry["created_at"],
            "experiment_set_id": entry["experiment_set_id"],
            "experiment_set_name": entry["experiment_set_name"],
            f"{format_column_name(metric_name)} Score": entry["main_metric_score"],
        }

        for metric, score in entry["other_metrics"].items():
            processed_entry[format_column_name(metric)] = score

        tokens_per_second = calculate_tokens_per_second(
            entry["other_metrics"].get("nb_tokens_completion"),
            entry["other_metrics"].get("generation_time"),
        )
        processed_entry["tokens_per_second"] = tokens_per_second
            
        entries.append(processed_entry)

    if not entries:
        return None

    df = pd.DataFrame(entries)
    df = add_repeat_column(df)

    score_column = f"{format_column_name(metric_name)} Score"

    df_repeat_true = df[df['repeat'] == True]
    df_repeat_false = df[df['repeat'] == False]
    df_repeat_false[f"{score_column}_mean"] = df_repeat_false[score_column]

    #if repeat, format like Experiment_set view
    if not df_repeat_true.empty:
        first_columns = ['Model', 'Model_renamed', 'Parameters', 'Created at', 'experiment_set_id', 'experiment_set_name']
        numeric_columns = df_repeat_true.select_dtypes(include=[np.number]).columns
        
        grouped = df_repeat_true.groupby("Model_renamed").agg({
            **{col: 'first' for col in first_columns},
            **{col: ['mean', 'std'] for col in numeric_columns if col not in first_columns}
        })
        
        result_repeat_true = pd.DataFrame()
        
        for col in first_columns:
            result_repeat_true[col] = grouped[col]
        
        for column in numeric_columns:
            if column not in first_columns:
                mean = grouped[(column, 'mean')].round(2)
                std = grouped[(column, 'std')].round(2)
                result_repeat_true[f"{column}_mean"] = mean
                result_repeat_true[column] = mean.astype(str) + " ± " + std.astype(str)
        
        result_repeat_true.reset_index(drop=True, inplace=True)
    else:
        result_repeat_true = pd.DataFrame()

    final_df = pd.concat([df_repeat_false, result_repeat_true], ignore_index=True)

    #sort by metric
    if f"{score_column}_mean" in final_df.columns:
        sort_column = f"{score_column}_mean"
    else:
        sort_column = score_column

    final_df.sort_values(
        sort_column,
        ascending=False,
        na_position="last",
        inplace=True,
    )
    
    final_df.reset_index(drop=True, inplace=True)
    final_df["Rank"] = final_df.index + 1

    columns_to_drop = [col for col in final_df.columns if col.endswith('_mean')] + [
        'Experiment ID',
        'Experiment name',
        'Model_renamed',
        "experiment_set_name",
        'repeat'
    ]
    final_df.drop(columns=columns_to_drop, inplace=True)

    fixed_columns = [
        'Rank', 'Model', 'Parameters', 'Created at',
        score_column
    ]
    
    col_decision = [col for col in final_df.columns if col in metrics_list_for_decision]
    other_columns = [col for col in final_df.columns if col not in fixed_columns + col_decision]
    column_order = fixed_columns + col_decision + other_columns

    return final_df[[col for col in column_order if col in final_df.columns]]


def display_dataset_and_metrics(product_info: dict, datasets: list[dict]) -> str:
    """Display dataset information and product metrics side by side."""
    col1, col2 = st.columns(2)

    with col1:
        st.write("#### Dataset")
        dataset_info = product_info.get("dataset", {})
        st.write(f"**Name:** {dataset_info.get('name', 'N/A')}")

        product_dataset_name = dataset_info.get("name")
        default_metric = DEFAULT_METRIC

        if product_dataset_name and datasets:
            for dataset in datasets:
                if dataset["name"] == product_dataset_name:
                    default_metric = dataset.get("default_metric", DEFAULT_METRIC)
                    break

        st.write(f"**Default metric:** {default_metric}")

    with col2:
        st.write("#### Necessary metrics for decision")
        if "metrics" not in product_info or not product_info["metrics"]:
            st.info("No metrics available for this product")
        else:
            metrics_list = [metric.replace('_', ' ').capitalize() for metric in product_info["metrics"]]
            st.write(", ".join(metrics_list))

    return default_metric

def get_base_url():
    query_params = st.query_params
    
    base_url = f"{st.get_option('server.baseUrlPath')}"
    
    if not base_url:
        base_url = "/"
    
    return base_url

def main() -> None:
    st.title("Products Metrics Leaderboard")

    product_config = load_product_config()

    if not product_config.get("products"):
        st.warning("No products configured yet.")
        return

    product_tabs = st.tabs(
        [product_info["name"] for product_info in product_config["products"].values()]
    )

    for tab, product_info in zip(product_tabs, product_config["products"].values()):
        with tab:
            st.header(f"{product_info['name'].replace('_', ' ')}")

            datasets = fetch_datasets()
            default_metric = display_dataset_and_metrics(product_info, datasets)

            st.divider()

            #model in production
            if "production_model" in product_info:
                display_model_production(product_info["production_model"], default_metric)
            else:
                st.warning("No production model information available")

            #models tests in exp
            current_model_id = (
                product_info.get("production_model", {})
                .get("current", {})
                .get("id")
            )
            product_dataset_name = product_info.get("dataset", {}).get("name")
            metrics_list_for_decision = ", ".join([metric for metric in product_info["metrics"]])

            leaderboard_data = fetch_leaderboard(default_metric, product_dataset_name) 
            df_leaderboard = process_leaderboard_data(
                leaderboard_data, default_metric, metrics_list_for_decision, current_model_id 
            )

            if df_leaderboard is not None:
                base_url = get_base_url()
                experiments_url = f"{base_url}experiments_set?expset="

                def create_link(experiment_set_id):
                    if pd.isna(experiment_set_id) or experiment_set_id == "" or experiment_set_id is None:
                        return None
                    else:
                        try:
                            return f"{experiments_url}{int(experiment_set_id)}"
                        except (ValueError, TypeError):
                            return None 

                df_leaderboard["Experiment Set Link"] = df_leaderboard["experiment_set_id"].apply(create_link)
                df_leaderboard.drop(columns="experiment_set_id", inplace=True)

                st.write("#### Leaderboard")
                st.data_editor(
                    df_leaderboard,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Experiment Set Link": st.column_config.LinkColumn(
                            "Experiment Set Link"
                        )
                    },
                )
            else:
                st.write("No data available for the leaderboard.")


main()
