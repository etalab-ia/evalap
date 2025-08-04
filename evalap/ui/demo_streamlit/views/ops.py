from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import fetch
from collections import defaultdict


def calculate_lightbulb_consumption(impact_energy_value):
    watthours = impact_energy_value * 1000
    consumption_hours = watthours / 5
    consumption_days = watthours / (5 * 24)
    consumption_minutes = watthours * 60 / 5
    consumption_seconds = watthours * 60 * 60 / 5

    if consumption_days >= 1:
        return int(consumption_days), "j"
    elif consumption_hours >= 1:
        return int(consumption_hours), "h"
    elif consumption_minutes >= 1:
        return int(consumption_minutes), "min"
    else:
        return int(consumption_seconds), "s"


def calculate_streaming_hours(impact_gwp_value_or_range):
    if hasattr(impact_gwp_value_or_range, "min"):
        impact_gwp_value = (impact_gwp_value_or_range.min + impact_gwp_value_or_range.max) / 2
    else:
        impact_gwp_value = impact_gwp_value_or_range

    streaming_hours = (impact_gwp_value * 10000) / 317

    if streaming_hours >= 24:
        return int(streaming_hours / 24), "j"
    elif streaming_hours >= 1:
        return int(streaming_hours), "h"
    elif streaming_hours * 60 >= 1:
        return int(streaming_hours * 60), "min"
    else:
        return int(streaming_hours * 60 * 60), "s"


def get_answer_emission_metrics(ops_eco, source):
    energy = ops_eco[source]["total_emissions"]["energy"]
    gwp = ops_eco[source]["total_emissions"]["gwp"]
    raw_date = ops_eco[source]["first_emission_date"]

    date_obj = datetime.fromisoformat(raw_date)
    pretty_date = date_obj.strftime("%d %B %Y")
    return energy, gwp, pretty_date


def main():
    st.title("Ops Analysis Dashboard")
    st.write("")

    # Global OPS metrics
    ops_metrics = fetch("get", "/ops_metrics")
    st.subheader("Global")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Experiment Sets", ops_metrics["experiment_sets"])
    col2.metric("Unique Experiments", ops_metrics["unique_experiments"])
    col3.metric("Unique Answers", ops_metrics["unique_answers"])
    col4.metric("Unique Metrics", ops_metrics["unique_metrics"])
    col5.metric("Unique Observations", ops_metrics["unique_observations"])

    st.write("---")

    st.subheader("Environmental impact")
    ops_eco = fetch("get", "/ops_eco")

    st.markdown('<h4 style="color: blue;">Responses generated</h4>', unsafe_allow_html=True)
    if ops_eco["answers"]["total_entries_with_emissions"] > 0:
        energy, gwp, pretty_date = get_answer_emission_metrics(ops_eco, "answers")

        # Calculating equivalence
        lightbulb_value, lightbulb_unit = calculate_lightbulb_consumption(energy)
        streaming_value, streaming_unit = calculate_streaming_hours(gwp)

        col_eco1, col_eco2, col_eco3, col_eco4, col_eco5 = st.columns(5)
        col_eco1.metric("Energy (kWh)", f"{energy:.4f}")
        col_eco2.metric("GWP (kgCO₂e)", f"{gwp:.4f}")
        col_eco3.metric("= 5W LED bulb", f"{lightbulb_value} {lightbulb_unit}")
        col_eco4.metric("= Video streaming", f"{streaming_value} {streaming_unit}")
        col_eco5.metric("Calculations since", pretty_date)

        st.caption(":bulb: **5W LED bulb**: equivalent lighting duration")
        st.caption(":tv: **Video streaming**: equivalent video streaming time (source: impactco2.fr)")

    else:
        st.write("No experiments with environmental impact calculations")

    st.markdown('<h4 style="color: blue;">Llms as-a-judge metrics</h4>', unsafe_allow_html=True)
    if ops_eco["observation_table"]["total_entries_with_emissions"] > 0:
        energy, gwp, pretty_date = get_answer_emission_metrics(ops_eco, "observation_table")

        # Calculating equivalence
        lightbulb_value, lightbulb_unit = calculate_lightbulb_consumption(energy)
        streaming_value, streaming_unit = calculate_streaming_hours(gwp)

        col_eco1, col_eco2, col_eco3, col_eco4, col_eco5 = st.columns(5)
        col_eco1.metric("Energy (kWh)", f"{energy:.4f}")
        col_eco2.metric("GWP (kgCO₂e)", f"{gwp:.4f}")
        col_eco3.metric("= 5W LED bulb", f"{lightbulb_value} {lightbulb_unit}")
        col_eco4.metric("= Video streaming", f"{streaming_value} {streaming_unit}")
        col_eco5.metric("Calculations since", pretty_date)

        st.caption(":bulb: **5W LED bulb**: equivalent lighting duration")
        st.caption(":tv: **Video streaming**: equivalent video streaming time (source: impactco2.fr)")

    else:
        st.write("No metrics with environmental impact calculations")

    st.write("---")

    models_by_provider = defaultdict(list)
    for model in ops_metrics["distinct_models"]:
        model_name = model.get("aliased_name") or model.get("name", "Unknown model")
        provider = model_name.split("/")[0] if "/" in model_name else "hybride"
        models_by_provider[provider].append(model_name)

    st.subheader("📈 Models Evaluated")
    for provider, models in models_by_provider.items():
        st.write(f"**{provider}**")
        for model in sorted(models):
            st.write(f"- {model}")
        st.write("---")


main()
