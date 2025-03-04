import streamlit as st
import pandas as pd
import plotly.express as px
from utils import fetch
from io import StringIO
import numpy as np
import re
from collections import defaultdict
from copy import deepcopy
from datetime import datetime

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
        observation_length=sum(exp["dataset"]["size"]*exp["num_metrics"] for exp in expset["experiments"]),
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

    fig = px.bar(
        report_df,
        x="Experiment Set Name",
        y=["Answer Successes", "Observation Successes"],
        title="Experiment Set Successes",
        barmode="group",
    )
    st.plotly_chart(fig, use_container_width=True)

def main():
    experiment_sets = fetch("get", "/experiment_sets")

    if not experiment_sets:
        st.warning("No experiment sets found.")
        return

    st.header("Experiment Set Status Report")
    create_status_report(experiment_sets)

    st.divider()

    st.write("TO DO : ")
    st.write("Status by model ")
    st.write("Status by metric")
    st.write(experiment_sets)

main()
