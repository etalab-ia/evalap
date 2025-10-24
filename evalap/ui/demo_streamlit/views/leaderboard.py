from itertools import groupby
from operator import itemgetter

import pandas as pd
import streamlit as st
from utils import calculate_tokens_per_second, fetch

DEFAULT_METRIC = "judge_notator"


@st.cache_data(ttl=300)
def fetch_leaderboard(metric_name: str = DEFAULT_METRIC, dataset_name: str | None = None) -> dict:
    endpoint = "/leaderboard"
    params = {"metric_name": metric_name}
    if dataset_name:
        params["dataset_name"] = dataset_name
    return fetch("get", endpoint, params)


@st.cache_data(ttl=3600)
def fetch_metrics() -> list[dict]:
    return fetch("get", "/metrics")


def fetch_datasets() -> list[dict]:
    return fetch("get", "/datasets")


def format_column_name(name: str) -> str:
    return name.replace("_", " ").title()


def group_datasets(datasets: list[str]) -> dict[str, list[str]]:
    return {k: sorted([v for v in datasets if v.startswith(k)]) for k in sorted(set(dataset.split("_")[0] for dataset in datasets))}


def create_ui_elements(
    group: str,
    available_metrics: list[str],
    datasets_in_group: list[str],
    group_index: int,
    grouped_metrics: dict[str, list[dict]],
) -> tuple[str, str, int, int, dict]:
    col1, col2, _, col3, col4 = st.columns([3, 3, 3, 2, 1])

    with col1:
        metric_name = st.selectbox(f"Select a metric for {group}", available_metrics, index=0)

    with col2:
        dataset_name = st.selectbox(f"Select a dataset for {group}", ["All"] + datasets_in_group, index=0)

    with col3:
        current_page = st.session_state.get(f"page_{group}", 1)
        page_input = st.number_input("Page", min_value=1, value=current_page, key=f"page_input_{group}")

    with col4:
        rows_per_page = st.selectbox("Rows per page", options=[10, 20, 30], index=0, key=f"rows_per_page_{group_index}")

    dataset_filter = None if dataset_name == "All" else dataset_name
    leaderboard_data = fetch_leaderboard(metric_name, dataset_filter)

    return metric_name, dataset_name, page_input, rows_per_page, leaderboard_data


def process_leaderboard_data(leaderboard_data: dict, group: str, metric_name: str, grouped_metrics: dict[str, list[dict]]) -> pd.DataFrame | None:
    tokens_completion_group = next(
        (group for group, metrics in grouped_metrics.items() if any(metric["name"] == "nb_tokens_completion" for metric in metrics)),
        "Ops",
    )

    entries = []
    for entry in leaderboard_data["entries"]:
        if entry["dataset_name"].startswith(group):
            params = f"{entry['sampling_param']} {entry['extra_param']}".strip()
            processed_entry = {
                "Rank": 0,
                "Experiment ID": entry["experiment_id"],
                "Model": entry["model_name"],
                "Parameters": params,
                "Dataset": entry["dataset_name"],
                f"{format_column_name(metric_name)} Score": entry["main_metric_score"],
            }

            for metric_type, metrics in grouped_metrics.items():
                for metric in metrics:
                    if metric["name"] in entry["other_metrics"]:
                        processed_entry[f"{metric_type.capitalize()} - {format_column_name(metric['name'])}"] = entry["other_metrics"][metric["name"]]

            tokens_per_second = calculate_tokens_per_second(
                entry["other_metrics"].get("nb_tokens_completion"),
                entry["other_metrics"].get("generation_time"),
            )
            processed_entry[f"{tokens_completion_group.capitalize()} - Tokens Per Second"] = tokens_per_second

            entries.append(processed_entry)

    if not entries:
        return None

    df = pd.DataFrame(entries)
    df.sort_values(f"{format_column_name(metric_name)} Score", ascending=False, na_position="last", inplace=True)
    df.reset_index(drop=True, inplace=True)
    df["Rank"] = df.index + 1

    fixed_columns = [
        "Rank",
        "Experiment ID",
        "Model",
        "Parameters",
        "Dataset",
        f"{format_column_name(metric_name)} Score",
    ]

    llm_columns = [col for col in df.columns if col.startswith("Llm - ")]
    ops_columns = [col for col in df.columns if col.startswith("Ops - ")]
    deepeval_columns = [col for col in df.columns if col.startswith("Deepeval - ")]
    other_columns = [col for col in df.columns if col not in fixed_columns + llm_columns + ops_columns + deepeval_columns]

    column_order = fixed_columns + llm_columns + ops_columns + deepeval_columns + other_columns

    df = df[[col for col in column_order if col in df.columns]]

    return df


def main():
    st.title("Evalap Leaderboard")

    metrics = fetch_metrics()
    datasets = fetch_datasets()

    if not metrics or not datasets:
        st.error("Unable to fetch metrics or datasets. Please try again later.")
        return

    filtered_metrics = [metric for metric in metrics if metric["type"] != "dataset"]
    sorted_metrics = sorted(filtered_metrics, key=itemgetter("type"))
    grouped_metrics = {k: list(v) for k, v in groupby(sorted_metrics, key=itemgetter("type"))}
    available_metrics = [metric["name"] for metrics in grouped_metrics.values() for metric in metrics]

    if DEFAULT_METRIC in available_metrics:
        available_metrics.insert(0, available_metrics.pop(available_metrics.index(DEFAULT_METRIC)))

    grouped_datasets = group_datasets([dataset["name"] for dataset in datasets])

    tabs = st.tabs(list(grouped_datasets.keys()))

    for group_index, (group_label, datasets_in_group) in enumerate(grouped_datasets.items()):
        with tabs[group_index]:
            metric_name, dataset_name, current_page_input, rows_per_page, leaderboard_data = create_ui_elements(
                group_label.split()[0], available_metrics, datasets_in_group, group_index, grouped_metrics
            )

            st.write(f"## 🏆 Top Performing LLMs - {metric_name.replace('_', ' ').title()}")
            if dataset_name != "All":
                st.write(f"Dataset: {dataset_name}")

            df = process_leaderboard_data(leaderboard_data, group_label.split()[0], metric_name, grouped_metrics)

            if df is not None and not df.empty:
                total_entries = len(df)
                num_pages = (total_entries - 1) // rows_per_page + 1
                current_page = min(current_page_input, num_pages)
                st.session_state[f"page_{group_label.split()[0]}"] = current_page

                start_idx = (current_page - 1) * rows_per_page
                end_idx = start_idx + rows_per_page

                st.dataframe(df.iloc[start_idx:end_idx], use_container_width=True, hide_index=True)

                st.write(f"Page {current_page} of {num_pages}")
            else:
                st.write(f"No experiments found for the selected criteria in {group_label.split()[0]}.")


main()
