import numpy as np
import pandas as pd
from datetime import datetime
import streamlit as st
from utils import fetch
from io import StringIO


def get_experiment_data(exp_id):
    """
    for each exp_id, returns query, answer true, answer llm and metrics
    """
    response = fetch("get", f"/experiment/{exp_id}", {"with_dataset": "true"})
    if not response:
        return None

    df = pd.read_json(StringIO(response["dataset"]["df"]))

    if "answers" in response:
        answers = {answer["num_line"]: answer["answer"] for answer in response["answers"]}
        df["answer"] = df.index.map(answers)

    if "results" in response:
        for result in response["results"]:
            metric_name = result["metric_name"]
            observations = {obs["num_line"]: obs["score"] for obs in result["observation_table"]}
            df[f"result_{metric_name}"] = df.index.map(observations)

    dataset_name = response.get("dataset", {}).get("name", "Unknown Dataset")
    model_name = response.get("model", {}).get("name", "Unknown Model")

    return df, dataset_name, model_name


def display_experiment_set_overview(expset, experiments_df):
    """
    returns a dataframe with the list of Experiments and the associated status
    """
    st.write(f"## Overview of experiment set: {expset['name']}")
    st.write(f"experiment_set id: {expset['id']}")

    row_height = 35
    header_height = 35
    border_padding = 5
    dynamic_height = len(experiments_df) * row_height + header_height + border_padding

    st.dataframe(
        experiments_df,
        use_container_width=True,
        hide_index=True,
        height=dynamic_height,
        column_config={"Id": st.column_config.TextColumn(width="small")},
    )


def display_experiment_set_result_(expset, experiments_df):
    st.write("## Results of the Experiment Set")

    total_experiments = len(experiments_df)
    total_success = experiments_df["Num success"].sum()

    st.write(f"Total Experiments: {total_experiments}")
    st.write(f"Total Successful Experiments: {total_success}")


def display_experiment_sets(experiment_sets):
    """
    returns the list of experiments set, with their status/info
    """
    cols = st.columns(3)
    for idx, exp_set in enumerate(experiment_sets):
        total_tries = sum(exp["num_try"] for exp in exp_set["experiments"])
        total_successes = sum(exp["num_success"] for exp in exp_set["experiments"])

        status = "OK" if total_tries == total_successes else "FAILURE"
        status_color = "green" if status == "OK" else "orange"

        when = datetime.fromisoformat(exp_set["created_at"]).strftime("%d %B %Y")

        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(
                    f"<div style='position: absolute; top: 10px; right: 10px; "
                    f"width: 10px; height: 10px; border-radius: 50%; "
                    f"background-color: {status_color};' "
                    f"title='{status}'></div>",
                    unsafe_allow_html=True,
                )

                if st.button(f"{exp_set['name']}", key=f"exp_set_{idx}"):
                    st.session_state["experimentset"] = exp_set
                    st.rerun()

                st.markdown(exp_set.get("readme", "No description available"))

                col1, col2, col3 = st.columns([1 / 6, 2 / 6, 3 / 6])
                with col1:
                    st.caption(f'id: {exp_set["id"]} ')
                with col2:
                    st.caption(f'Experiments: {len(exp_set["experiments"])} ')
                with col3:
                    st.caption(f"Created on {when}")

                if status == "FAILURE":
                    with st.expander("Failure Analysis", expanded=False):
                        for exp in exp_set["experiments"]:
                            if exp["num_try"] == exp["num_success"]:
                                continue
                            st.write(f"{exp['id']} {exp['name']}")


def display_experiment_details(experimentset, experiments_df):
    experiment_ids = experiments_df["Id"].tolist()
    selected_exp_id = st.selectbox("Select Experiment ID", experiment_ids)
    if selected_exp_id:
        df_with_results, dataset_name, model_name = get_experiment_data(selected_exp_id)
        if df_with_results is not None:
            st.write(f"### Detailed results of the experiment id={selected_exp_id} ")
            st.write(f"**Dataset:** {dataset_name}")
            st.write(f"**Model:** {model_name}")
            st.dataframe(df_with_results)
        else:
            st.error("Failed to fetch experiment data")


def process_experiment_results(experimentset):
    """
    Process experiment results dynamically across different experiment types.
    
    Args:
        experimentset (dict): The experiment set containing experiment details

    Returns:
        pd.DataFrame: A processed DataFrame with experiment results
    """
    rows = []
    metrics = set() 

    for exp in experimentset.get("experiments", []):
        if exp["experiment_status"] != "finished":
            st.warning(f"Warning: experiment {exp['id']} is not finished yet...")
        
        response = fetch("get", f"/experiment/{exp['id']}", {"with_dataset": "true"})

        if not response:
            continue

        model_name = response["model"]["name"]
        extra_params = response["model"].get("extra_params", {})

        # Determine experiment variant (e.g., RAG limit, repeat, etc.)
        variant = _extract_experiment_variant(extra_params)

        row = {"model": f"{model_name}_{variant}" if variant else model_name}

        for metric_results in response.get("results", []):
            metric = metric_results["metric_name"]
            metrics.add(metric)

            scores = np.array([
                x["score"] for x in metric_results["observation_table"] 
                if pd.notna(x.get("score"))
            ])

            if len(scores) > 0:
                row[f"{metric}_mean"] = np.mean(scores)
                row[f"{metric}_std"] = np.std(scores)
                row[f"{metric}_median"] = np.median(scores)
                row[f"{metric}_mean_std"] = f"{scores.mean():.2f} ± {scores.std():.2f}"
                row[f"{metric}_support"] = len(scores)

        rows.append(row)

    if not rows:
        st.error("No valid experiment results found")
        return None

    df = pd.DataFrame(rows)
    
    default_sort_metric = _find_default_sort_metric(metrics)
    if default_sort_metric and default_sort_metric in df.columns:
        df = df.sort_values(by=default_sort_metric, ascending=False)

    return df

def _extract_experiment_variant(extra_params: dict):
    """
    Extract a meaningful variant identifier from extra parameters.
    """
    if not extra_params:
        return ""
    
    if "rag" in extra_params:
        if "limit" in extra_params["rag"]:
            return f"limit_{extra_params['rag']['limit']}"
    
    return str(list(extra_params.keys())[0]) if extra_params else ""

def _find_default_sort_metric(metrics):
    """
    Find a sensible default metric for sorting results.
    """
    preferred_metrics = ['judge_exactness', 'contextual_relevancy']
    for metric in preferred_metrics:
        if metric in metrics:
            return f"{metric}_mean"
    
    return list(metrics)[0] + "_mean" if metrics else None

def display_experiment_results(experimentset):
    results_df = process_experiment_results(experimentset)
    
    if results_df is not None:
        st.write("## Experiment Results")
        st.dataframe(results_df)


def display_experiment_set_result(experimentset, experiments_df):
    st.write("## Results of the Experiment Set")

    if experiments_df["Num success"].sum() == experiments_df["Num try"].sum():
        display_experiment_results(experimentset)
        total_experiments = len(experiments_df)
        total_success = experiments_df["Num success"].sum()
        st.write(f"Total Experiments: {total_experiments}")
        st.write(f"Total Successful Experiments: {total_success}")
    else:
        st.error("Results cannot be displayed as not all experiments are in Success")


def main():
    if st.session_state.get("experimentset"):
        experimentset = st.session_state["experimentset"]
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button(":arrow_left: Go back", key="go_back"):
                st.session_state["experimentset"] = None
                st.rerun()

        with col2:
            if st.button("🔄 Refresh Data"):
                expid = experimentset["id"]
                experimentset = fetch("get", f"/experiment_set/{expid}")
                if not experimentset:
                    raise ValueError("experimentset not found: %s" % expid)
                st.session_state["experimentset"] = experimentset

        # Build the expset dataframe
        experiments_df = pd.DataFrame(
            [
                {
                    "Id": exp["id"],
                    "Name": exp["name"],
                    "Status": exp["experiment_status"],
                    "Created at": exp["created_at"],
                    "Num try": exp["num_try"],
                    "Num success": exp["num_success"],
                }
                for exp in experimentset.get("experiments", [])
            ]
        )
        experiments_df.sort_values(by="Id", ascending=True, inplace=True)

        tab1, tab2, tab3 = st.tabs(["Set Overview", "Results", "Detail by experiment id"])

        def show_warning_in_tabs(message):
            with tab1:
                st.warning(message)
            with tab2:
                st.warning(message)
            with tab3:
                st.warning(message)

        df = experiments_df  # alias
        if df["Num success"].sum() != df["Num try"].sum() and (df["Status"] == "finished").all():
            show_warning_in_tabs("Warning: some experiments are failed.")
        if not (df["Status"] == "finished").all():
            show_warning_in_tabs("Warning: some experiments are not finished.")

        with tab1:
            display_experiment_set_overview(experimentset, experiments_df)
        with tab2:
            display_experiment_set_result(experimentset, experiments_df)
        with tab3:
            display_experiment_details(experimentset, experiments_df)

    else:
        st.title("Experiments (Set)")
        experiment_sets = fetch("get", "/experiment_sets")
        if experiment_sets:
            display_experiment_sets(experiment_sets)


main()
