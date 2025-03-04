import streamlit as st
import pandas as pd
import plotly.express as px
from utils import fetch
from collections import defaultdict
from datetime import datetime
from io import StringIO


def _get_expset_status(expset: dict) -> tuple[dict, dict]:
    """Determines the status and counts for an experiment set."""
    status_codes = {
        "pending": {"text": "Experiments did not start yet", "color": "yellow"},
        "running": {"text": "Experiments are running", "color": "orange"},
        "finished": {"text": "All experiments are finished", "color": "green"},
    }

    counts = dict(
        total_answer_tries=sum(exp["num_try"] for exp in expset["experiments"]),
        total_answer_successes=sum(exp["num_success"] for exp in expset["experiments"]),
        total_observation_tries=sum(exp["num_observation_try"] for exp in expset["experiments"]),
        total_observation_successes=sum(exp["num_observation_success"] for exp in expset["experiments"]),
        answer_length=sum(exp["dataset"]["size"] for exp in expset["experiments"]),
        observation_length=sum(exp["dataset"]["size"] * exp["num_metrics"] for exp in expset["experiments"]),
    )

    if all(exp["experiment_status"] == "pending" for exp in expset["experiments"]):
        status = status_codes["pending"]
    elif all(exp["experiment_status"] == "finished" for exp in expset["experiments"]):
        status = status_codes["finished"]
    else:
        status = status_codes["running"]

    return status, counts


def create_status_report(experiment_sets):
    """
    Generates a DataFrame report with experiment set statuses and displays it,
    along with a bar chart visualization.
    """
    st.subheader("Status by Experiment Set")

    report_data = []
    for exp_set in experiment_sets:
        status, counts = _get_expset_status(exp_set)
        has_failure = counts["total_observation_tries"] > counts["total_observation_successes"]

        report_data.append({
            "Experiment Set Name": exp_set["name"],
            "Status": status["text"],
            "Total Experiments": len(exp_set["experiments"]),
            "Answer Tries": counts["total_answer_tries"],
            "Answer Successes": counts["total_answer_successes"],
            "Observation Tries": counts["total_observation_tries"],
            "Observation Successes": counts["total_observation_successes"],
            "Has Failure": has_failure,
        })

    report_df = pd.DataFrame(report_data)

    st.dataframe(
        report_df,
        use_container_width=True,
        hide_index=True,
    )


def _get_experiment_data(exp_id):
    """
    for each exp_id, returns query, answer true, answer llm and metrics
    """
    exp = fetch("get", f"/experiment/{exp_id}", {"with_dataset": "true"})
    if not exp:
        return None

    df = pd.read_json(StringIO(exp["dataset"]["df"]))

    if "answers" in exp:
        answers = {answer["num_line"]: answer["answer"] for answer in exp["answers"]}
        df["answer"] = df.index.map(answers)

    if "results" in exp:
        for result in exp["results"]:
            metric_name = result["metric_name"]
            observations = {obs["num_line"]: obs["score"] for obs in result["observation_table"]}
            df[f"result_{metric_name}"] = df.index.map(observations)

    return exp


def analyze_by_model_and_metric(experiment_sets):
    """Analyzes experiment statuses by model and metric, including failed experiments and failure rates."""
    model_data = defaultdict(lambda: {"finished": 0, "running": 0, "pending": 0, "failed": 0, "no_failed": 0})
    metric_data = defaultdict(lambda: {"finished": 0, "running": 0, "pending": 0, "failed": 0, "no_failed": 0})

    for exp_set in experiment_sets:
        for exp in exp_set["experiments"]:
            exp_id = exp["id"]
            experiment = _get_experiment_data(exp_id)

            if experiment:
                # Determine model name
                model_name = experiment.get("model", {}).get("name", "Unknown Model")

                # Check for errors in answers
                has_error = any(answer.get("error_msg") for answer in experiment.get("answers", []))

                if has_error:
                    model_data[model_name]["failed"] += 1
                else:
                    status = experiment["experiment_status"]
                    model_data[model_name][status] += 1
                    model_data[model_name]["no_failed"] += 1

                    # Process metrics analysis ONLY when there's no error
                    if "results" in experiment:
                        for result in experiment["results"]:
                            metric_name = result["metric_name"]
                            metric_status = result["metric_status"]
                            metric_data[metric_name][metric_status] += 1
                            metric_data[metric_name]["no_failed"] += 1
                    elif has_error:
                        metric_data["Unknown"]["failed"] += 1

    def calculate_failure_rate(row):
        total = row['failed'] + row['no_failed']
        return row['failed'] / total if total > 0 else 0

    model_report = pd.DataFrame.from_dict(model_data, orient="index")
    model_report["Total"] = model_report[["finished", "running", "pending"]].sum(axis=1)
    model_report["Failure Rate"] = model_report.apply(calculate_failure_rate, axis=1)

    columns_order = ["finished", "running", "pending", "Total", "failed", "no_failed", "Failure Rate"]
    model_report = model_report[columns_order]
    model_for_graph = model_report.copy()

    model_report.columns = pd.MultiIndex.from_tuples([
        ("Status", "finished"), ("Status", "running"), ("Status", "pending"), ("Status", "Total"),
        ("Failure Analysis", "failed"), ("Failure Analysis", "no_failed"), ("Failure Analysis", "Failure Rate")
    ])

    st.subheader("Experiment Status by Model")
    st.dataframe(model_report, use_container_width=True)

    fig_model = px.bar(
        model_for_graph,
        x=model_for_graph.index,
        y=["finished", "running", "pending", "failed"],
        title="Experiment Status by Model",
        labels={"value": "Count", "index": "Model"},
    )
    st.plotly_chart(fig_model, use_container_width=True)

    fig_model_failure = px.bar(
        model_for_graph,
        x=model_for_graph.index,
        y="Failure Rate",
        title="Failure Rate by Model",
        labels={"Failure Rate": "Failure Rate", "index": "Model"},
    )
    st.plotly_chart(fig_model_failure, use_container_width=True)

    metric_report = pd.DataFrame.from_dict(metric_data, orient="index")
    metric_report["Total"] = metric_report[["finished", "running", "pending", "failed"]].sum(axis=1)
    metric_report["Failure Rate"] = metric_report.apply(calculate_failure_rate, axis=1)
    st.subheader("Experiment Status by Metric")
    st.dataframe(metric_report, use_container_width=True)

    fig_metric = px.bar(
        metric_report,
        x=metric_report.index,
        y=["finished", "running", "pending", "failed"],
        title="Experiment Status by Metric",
        labels={"value": "Count", "index": "Metric"},
    )
    st.plotly_chart(fig_metric, use_container_width=True)

    fig_metric_failure = px.bar(
        metric_report,
        x=metric_report.index,
        y="Failure Rate",
        title="Failure Rate by Metric",
        labels={"Failure Rate": "Failure Rate", "index": "Metric"},
    )
    st.plotly_chart(fig_metric_failure, use_container_width=True)


def main():
    experiment_sets = fetch("get", "/experiment_sets")

    if not experiment_sets:
        st.warning("No experiment sets found.")
        return

    st.title("Ops Analysis")

    create_status_report(experiment_sets)

    analyze_by_model_and_metric(experiment_sets)


main()
