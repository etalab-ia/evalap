import pandas as pd
import streamlit as st
from utils import fetch
from operator import itemgetter
from itertools import groupby

# Metric used by default, can be overridden in the UI
DEFAULT_METRIC = "judge_notator"

# Cache API calls to improve performance
@st.cache_data(ttl=300)
def fetch_leaderboard(metric_name=DEFAULT_METRIC, dataset_name=None):
    endpoint = "/leaderboard"
    params = {"metric_name": metric_name}
    if dataset_name:
        params["dataset_name"] = dataset_name
    return fetch("get", endpoint, params)

@st.cache_data(ttl=3600)
def fetch_metrics():
    return fetch("get", "/metrics")

def fetch_datasets():
    return fetch("get", "/datasets")

def calculate_tokens_per_second(tokens, time):
    # Avoid division by zero and handle None values
    if tokens is not None and time is not None and time != 0:
        return round(tokens / time, 1)  
    return None

def format_column_name(name):
    return name.replace("_", " ").title()

def group_datasets(datasets):
    # Group datasets by their product (first part of the name before '_')
    return {k: list(v) for k, v in groupby(sorted(datasets, key=lambda x: x.split('_')[0]), key=lambda x: x.split('_')[0])}

def main():
    st.title("EG1 Leaderboard")
    
    # Fetch initial data
    metrics = fetch_metrics()
    datasets = fetch_datasets()
    
    if not metrics or not datasets:
        st.error("Unable to fetch metrics or datasets. Please try again later.")
        return

    # Process metrics data
    filtered_metrics = [metric for metric in metrics if metric["type"] != "dataset"]
    sorted_metrics = sorted(filtered_metrics, key=itemgetter("type"))
    grouped_metrics = {k: list(v) for k, v in groupby(sorted_metrics, key=itemgetter("type"))}
    
    available_metrics = [metric["name"] for metrics in grouped_metrics.values() for metric in metrics]
    available_datasets = [dataset["name"] for dataset in datasets]
    
    # Ensure default metric is first in the list
    if DEFAULT_METRIC in available_metrics:
        available_metrics.insert(0, available_metrics.pop(available_metrics.index(DEFAULT_METRIC)))
    
    # Group datasets by product
    grouped_datasets = group_datasets(available_datasets)
    
    # Create tabs for each product
    tabs = st.tabs(list(grouped_datasets.keys()))
    
    for tab, (group, datasets_in_group) in zip(tabs, grouped_datasets.items()):
        with tab:
            # Initial fetch with default metric
            leaderboard_data = fetch_leaderboard(DEFAULT_METRIC)
            
            # Filter entries for the current group
            group_entries = [
                entry for entry in leaderboard_data.get("entries", [])
                if entry["dataset_name"].startswith(group)
            ]
            
            if group_entries:
                # UI elements for user interaction
                col1, col2, col3 = st.columns([3, 3, 2])  
                
                with col1:
                    metric_name = st.selectbox(f"Select a metric for {group}", available_metrics, index=0, key=f"metric_{group}")

                with col2:
                    dataset_name = st.selectbox(f"Select a dataset for {group}", ["All"] + datasets_in_group, index=0, key=f"dataset_{group}")

                with col3:
                    current_page = st.session_state.get(f'page_{group}', 1)
                    page_input = st.number_input('Page', min_value=1, value=current_page, key=f"page_input_{group}")

                dataset_filter = None if dataset_name == "All" else dataset_name
                
                # Fetch new data only if necessary
                if metric_name != DEFAULT_METRIC or dataset_filter:
                    leaderboard_data = fetch_leaderboard(metric_name, dataset_filter)
                
                st.write(f"## 🏆 Top Performing LLMs - {metric_name.replace('_', ' ').title()}")
                if dataset_filter:
                    st.write(f"Dataset: {dataset_filter}")
                st.write("")

                # Process leaderboard data
                df = pd.DataFrame([
                    {
                        "Experiment ID": entry["experiment_id"],
                        "Model": entry["model_name"],
                        "Sampling Param": entry["sampling_param"],
                        "Extra Param": entry["extra_param"],
                        "Dataset": entry["dataset_name"],
                        f"{format_column_name(metric_name)} Score": entry["main_metric_score"],
                        "Tokens Per Second": calculate_tokens_per_second(
                            entry["other_metrics"].get("nb_tokens_completion"),
                            entry["other_metrics"].get("generation_time")
                        ),
                        **{format_column_name(k): v for k, v in entry["other_metrics"].items() if k not in ["nb_tokens_completion", "generation_time"]}
                    }
                    for entry in leaderboard_data["entries"]
                    if entry["dataset_name"].startswith(group)
                ])

                if not df.empty:
                    # Sort and rank the data
                    df = df.sort_values(f"{format_column_name(metric_name)} Score", ascending=False, na_position='last')
                    df = df.reset_index(drop=True)
                    df.insert(0, 'Rank', df.index + 1)

                    if dataset_filter:
                        df = df.drop(columns=["Dataset"])

                    # Pagination logic
                    total_entries = len(df)
                    page_size = 10
                    num_pages = (total_entries - 1) // page_size + 1
                    current_page = min(page_input, num_pages)  
                    st.session_state[f'page_{group}'] = current_page
                    start_idx = (current_page - 1) * page_size
                    end_idx = start_idx + page_size

                    # Display the dataframe
                    st.dataframe(
                        df.iloc[start_idx:end_idx],
                        use_container_width=True,
                        hide_index=True
                    )

                    st.write(f"Page {current_page} of {num_pages}")
                else:
                    st.write(f"No experiments found for the selected criteria in {group}.")
            else:
                st.write(f"No experiments for {group}.")

main()
