from itertools import groupby
from operator import itemgetter
from pathlib import Path

import pandas as pd
import streamlit as st
import yaml

from utils import fetch, calculate_tokens_per_second

DEFAULT_METRIC = "judge_exactness"
CONFIG_PATH = Path(__file__).parent.parent.parent.parent / "config" / "products" / "product_config.yml"

#TODO:
# recup list mtetric du produit et n'afficher que les résultats dessus 


def load_product_config() -> dict:
    """Load product configuration from YAML file."""
    try:
        if not CONFIG_PATH.exists():
            st.error(f"Configuration file not found at: {CONFIG_PATH}")
            return {"products": {}}

        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        st.error(f"Error loading configuration: {str(e)}")
        return {"products": {}}


def fetch_experiment_results(exp_id: int) -> dict:
    """Fetch results for a single experiment."""
    return fetch("get", f"/experiment/{exp_id}", {"with_dataset": "true"})


@st.cache_data(ttl=300)
def fetch_leaderboard(metric_name: str = DEFAULT_METRIC, dataset_name: str | None = None) -> dict:
    """Fetch leaderboard data with caching."""
    endpoint = "/leaderboard"
    params = {"metric_name": metric_name}
    if dataset_name:
        params["dataset_name"] = dataset_name
    return fetch("get", endpoint, params)


def fetch_datasets() -> list[dict]:
    return fetch("get", "/datasets")


def display_model_production(model_info: dict) -> None:
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

        metrics_data = {"model_name": current_model.get("name", "N/A")}
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
                metrics_data[metric_name] = round(mean_score, 2)

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


def process_leaderboard_data(
    leaderboard_data: dict,
    metric_name: str,
    metrics_list_for_decision,
    current_model_id: int | None = None,
) -> pd.DataFrame | None :

    entries = []
    for entry in leaderboard_data["entries"]:
        if current_model_id and entry["experiment_id"] == current_model_id:
            continue

        params = f"{entry['sampling_param']} {entry['extra_param']}".strip()
        processed_entry = {
            "Rank": 0,
            "Experiment ID": entry["experiment_id"],
            "Model": entry["model_name"],
            "Parameters": params,
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
    df.sort_values(
        f"{format_column_name(metric_name)} Score",
        ascending=False,
        na_position="last",
        inplace=True,
    )
    df.reset_index(drop=True, inplace=True)
    df["Rank"] = df.index + 1

    fixed_columns = ['Rank', 'Experiment ID', 'Model', 'Parameters', f"{format_column_name(metric_name)} Score"]
    col_decision = [col for col in df.columns if col in metrics_list_for_decision]
    other_columns = [col for col in df.columns if col not in fixed_columns + col_decision]

    column_order = fixed_columns + col_decision + other_columns

    df = df[[col for col in column_order if col in df.columns]]

    return df


def format_column_name(name: str) -> str:
    """Format column names for better readability."""
    return name#.replace("_", " ").title()


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

def main() -> None:
    st.title("Product Metrics Dashboard")

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
                display_model_production(product_info["production_model"])
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

            if df_leaderboard is not None and not df_leaderboard.empty:
                st.write("#### Leaderboard")
                st.dataframe(df_leaderboard, use_container_width=True, hide_index=True)
            else:
                st.write("No data available for the leaderboard.")

main()
