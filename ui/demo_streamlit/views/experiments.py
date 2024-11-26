import streamlit as st
import pandas as pd
import numpy as np
from utils import fetch

def fetch_all_experiments():
    endpoint = "/experiments"
    return fetch("get", endpoint)

def fetch_experiment_results(exp_id):
    endpoint = f"/experiment/{exp_id}"
    params = {"with_results": "true"}
    return fetch("get", endpoint, params)

def process_experiment_results(experiment):
    results = experiment.get("results", [])
    df_metrics = {}
    
    for metric_results in results:
        metric_name = metric_results["metric_name"]
        arr = np.array([x["score"] for x in metric_results["observation_table"] if pd.notna(x["score"])])
        
        if len(arr) > 0:
            df = pd.DataFrame([[
                np.mean(arr),
                np.std(arr),
                np.median(arr),
                f"{arr.mean():.2f} ± {arr.std():.2f}",
                len(arr),
            ]], columns=["mean", "std", "median", "mean_std", "support"])
            
            df_metrics[metric_name] = df
    
    return pd.DataFrame({metric_name: df["mean_std"].iloc[0] for metric_name, df in sorted(df_metrics.items())}, index=[experiment["name"]])

def display_all_experiments():
    experiments = fetch_all_experiments()
    
    if not experiments:
        st.error("No experiments found.")
        return
    
    df = pd.DataFrame(experiments)
    
    st.dataframe(df)

def display_experiment_results(exp_id):
    experiment = fetch_experiment_results(exp_id)
    
    if not experiment:
        return
    
    if experiment["experiment_status"] != "finished":
        st.warning(f"Experiment {exp_id} is not finished yet...")
    
    results_df = process_experiment_results(experiment)
    
    if not results_df.empty:
        st.dataframe(results_df)
    else:
        st.info("No results available for this experiment.")

def main():
    st.title("Experiments")
    
    view_option = st.radio("Select View Option", ["View All Experiments", "View Experiment by ID"])
    
    if view_option == "View All Experiments":
        display_all_experiments()
    else:
        exp_id = st.number_input("Enter Experiment ID", min_value=1, step=1)
        if st.button("Show Results"):
            display_experiment_results(exp_id)


main()