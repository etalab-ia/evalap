import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from utils import fetch
from io import StringIO

# Constants for warning
FINISHED_STATUS = "finished"
UNKNOWN_DATASET = "Unknown Dataset"
UNKNOWN_MODEL = "Unknown Model"

@st.cache_data
def fetch_all_experiments() -> List[Dict]:
    return fetch("get", "/experiments")

@st.cache_data
def fetch_experiment_results(exp_id: int) -> Dict:
    return fetch("get", f"/experiment/{exp_id}", {"with_dataset": "true"})

def process_experiment_data(response: Dict) -> Tuple[Optional[pd.DataFrame], str, str]:
    if not response:
        return None, UNKNOWN_DATASET, UNKNOWN_MODEL

    df = pd.read_json(StringIO(response["dataset"]["df"]))

    if "answers" in response:
        df["answer"] = df.index.map({answer["num_line"]: answer["answer"] for answer in response["answers"]})

    if "results" in response:
        for result in response["results"]:
            metric_name = result["metric_name"]
            df[f"result_{metric_name}"] = df.index.map({obs["num_line"]: obs["score"] for obs in result["observation_table"]})

    return df, response.get("dataset", {}).get("name", UNKNOWN_DATASET), response.get("model", {}).get("name", UNKNOWN_MODEL)

def calculate_metric_stats(arr: np.array) -> Dict[str, float]:
    return {
        "mean": np.mean(arr),
        "std": np.std(arr),
        "median": np.median(arr),
        "mean_std": f"{arr.mean():.2f} ± {arr.std():.2f}",
        "support": len(arr)
    }

def process_experiment_results(experiment: Dict) -> pd.DataFrame:
    df_metrics = {
        metric_results["metric_name"]: pd.DataFrame([calculate_metric_stats(np.array([x["score"] for x in metric_results["observation_table"] if pd.notna(x["score"])]))]) 
        for metric_results in experiment.get("results", [])
        if len([x["score"] for x in metric_results["observation_table"] if pd.notna(x["score"])]) > 0
    }
    return pd.DataFrame(
        {metric_name: df["mean_std"].iloc[0] for metric_name, df in sorted(df_metrics.items())},
        index=[experiment["name"]]
    )

@st.cache_data
def preprocess_experiments(experiments: List[Dict]) -> pd.DataFrame:
    formatted_experiments = [
        {
            "id": exp["id"],
            "name": exp["name"],
            "dataset": exp["dataset"]["name"],
            "model": exp["model"]["name"] if exp["model"] else "N/A",
            **{f"{result['metric_name']}_score": f"{sum(obs['score'] for obs in result['observation_table'] if obs['score'] is not None) / len([obs for obs in result['observation_table'] if obs['score'] is not None]):.2f}"
               for result in exp.get("results", []) if any(obs['score'] is not None for obs in result['observation_table'])}
        }
        for exp in experiments
        if exp["experiment_status"] == FINISHED_STATUS and exp["experiment_set_id"] is None
    ]
    return pd.DataFrame(formatted_experiments)

def display_experiment_results(exp_id: int):
    experiment = fetch_experiment_results(exp_id)

    if not experiment:
        st.error(f"No results found for experiment {exp_id}")
        return

    if experiment["experiment_status"] != FINISHED_STATUS:
        st.warning(f"Experiment {exp_id} is not finished yet...")

    if experiment["num_success"] != experiment["num_try"]:
        st.warning("Warning: some experiments have failed.")
    if experiment["num_observation_success"] != experiment["num_observation_try"]:
        st.warning("Warning: some metrics have failed.")

    results_df = process_experiment_results(experiment)
    df_with_results, dataset_name, model_name = process_experiment_data(experiment)

    cols = st.columns(3)
    cols[0].write(f"**Dataset:** {dataset_name}")
    cols[1].write(f"**Model:** {model_name}")

    if not results_df.empty:
        st.subheader("Aggregated Results")
        st.dataframe(results_df)
        
        st.subheader("Detailed Results")
        st.dataframe(df_with_results)
    else:
        st.info("No results available for this experiment.")

def main():
    st.title("Experiments (not in a Set)")
    st.info("Here, you can see the experiments that are not in evaluation sets.")

    st.subheader("All Experiments (finished)")
    experiments = fetch_all_experiments()
    
    if not experiments:
        st.error("No experiments found.")
    else:
        df = preprocess_experiments(experiments)
        
        metric_columns = [col for col in df.columns if col.endswith("_score")]
        df = df[df[metric_columns].notna().any(axis=1)]

        st.dataframe(df)

        st.divider()

    if not df.empty:
        st.markdown("### Select a finished experiment to view details:")
        selected_exp_id = st.selectbox(
            label="",
            options=df["id"].tolist(),
            format_func=lambda x: f"Experiment {x}",
            label_visibility="collapsed"
        )
        if st.button("Show Selected Experiment Results"):
            display_experiment_results(selected_exp_id)
    else:
        st.info("No finished experiments found.")

main()

