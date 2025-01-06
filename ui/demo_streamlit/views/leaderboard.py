import pandas as pd
import streamlit as st
from utils import fetch
from operator import itemgetter
from itertools import groupby

DEFAULT_METRIC = "judge_notator"

@st.cache_data(ttl=600)
def fetch_leaderboard(metric_name="judge_notator", dataset_name=None):
    endpoint = "/leaderboard"
    params = {"metric_name": metric_name}
    if dataset_name:
        params["dataset_name"] = dataset_name
    return fetch("get", endpoint, params)

@st.cache_data(ttl=3600)
def fetch_metrics():
    return fetch("get", "/metrics")

@st.cache_data(ttl=3600)
def fetch_datasets():
    return fetch("get", "/datasets")

def calculate_tokens_per_second(tokens, time):
    if tokens is not None and time is not None and time != 0:
        return round(tokens / time, 1)  
    return None

def format_column_name(name):
    """Format the column name to remove underscores and capitalize each word."""
    return name.replace("_", " ").title()

def main():
    st.title("EG1 Leaderboard")
    
    metrics = fetch_metrics()
    datasets = fetch_datasets()
    
    if not metrics or not datasets:
        st.error("Unable to fetch metrics or datasets. Please try again later.")
        return

    filtered_metrics = [metric for metric in metrics if metric["type"] != "dataset"]
    sorted_metrics = sorted(filtered_metrics, key=itemgetter("type"))
    grouped_metrics = {k: list(v) for k, v in groupby(sorted_metrics, key=itemgetter("type"))}
    
    available_metrics = [metric["name"] for metrics in grouped_metrics.values() for metric in metrics]
    available_datasets = [dataset["name"] for dataset in datasets]
    
    if DEFAULT_METRIC in available_metrics:
        available_metrics.insert(0, available_metrics.pop(available_metrics.index(DEFAULT_METRIC)))
    
    col1, col2, col3 = st.columns([3, 3, 2])  
    
    with col1:
        metric_name = st.selectbox("Select a metric", available_metrics, index=0)

    with col2:
        dataset_name = st.selectbox("Select a dataset", ["All"] + available_datasets, index=0)

    with col3:
        current_page = st.session_state.get('page', 1)
        
        page_input = st.number_input('Page', min_value=1, value=current_page)

    dataset_filter = None if dataset_name == "All" else dataset_name
    
    st.write(f"## 🏆 Top Performing LLMs Leaderboard - {metric_name.replace('_', ' ').title()}")
    if dataset_filter:
        st.write(f"Dataset: {dataset_filter}")
    st.write("")

    leaderboard_data = fetch_leaderboard(metric_name, dataset_filter)

    if leaderboard_data and leaderboard_data["entries"]:
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
        ])

        df = df.sort_values(f"{format_column_name(metric_name)} Score", ascending=False, na_position='last')
        df = df.reset_index(drop=True)
        
        df.insert(0, 'Rank', df.index + 1)

        if dataset_filter:
            df = df.drop(columns=["Dataset"])

        total_entries = len(df)
        page_size = 10
        num_pages = (total_entries - 1) // page_size + 1
        
        current_page = min(page_input, num_pages)  
        st.session_state['page'] = current_page
        
        start_idx = (current_page - 1) * page_size
        end_idx = start_idx + page_size

        st.dataframe(
            df.iloc[start_idx:end_idx],
            use_container_width=True,
            hide_index=True
        )

        st.write(f"Page {current_page} of {num_pages}")
        
    else:
        st.write("No data available for the leaderboard.")

main()
