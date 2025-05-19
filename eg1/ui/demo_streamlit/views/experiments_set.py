import json
import re
import time
from collections import defaultdict
from copy import deepcopy
from datetime import datetime
from io import StringIO

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from utils import fetch, _rename_model_variants, _format_model_params


#
# Cached method for critical data fetching
#


def _fetch(method, endpoint, data=None, refresh=False):
    if refresh:
        __fetch.clear(method, endpoint, data)

    return __fetch(method, endpoint, data)


@st.cache_data(ttl=600, max_entries=10)
def __fetch(method, endpoint, data=None):
    return fetch(method, endpoint, data)


def _fetch_experimentset(expid, partial_expset, refresh=False, with_eco=False):
    if refresh:
        __fetch_experimentset.clear(expid, partial_expset, with_eco)
    return __fetch_experimentset(expid, partial_expset, with_eco)


@st.cache_data(ttl=600, max_entries=3)
def __fetch_experimentset(expid, partial_expset, with_eco=False, refresh=False):
    if refresh:
        _fetch_experimentset.clear(expid, partial_expset, with_eco)

    experimentset = partial_expset
    if not experimentset:
        raise ValueError("experimentset not found: %s" % expid)

    # Fetch experiment results ou eco
    for i, expe in enumerate(experimentset["experiments"]) or []:
        if with_eco:
            expe = fetch("get", f"/experiment/{expe['id']}", {"with_eco": True})
        else:
            expe = fetch("get", f"/experiment/{expe['id']}", {"with_results": True})
        if not expe:
            continue
        experimentset["experiments"][i] = expe

    return experimentset


#
# @TODO: codefactor and triage
#


def _get_expset_status(expset: dict) -> tuple[dict, dict]:
    status_codes = {
        "pending": {"text": "Experiments did not start yet", "color": "yellow"},
        "running": {"text": "Experiments are running", "color": "orange"},
        "finished": {"text": "All experiments are finished", "color": "green"},
    }

    counts = dict(
        total_answer_tries=sum(expe["num_try"] for expe in expset["experiments"]),
        total_answer_successes=sum(expe["num_success"] for expe in expset["experiments"]),
        total_observation_tries=sum(expe["num_observation_try"] for expe in expset["experiments"]),
        total_observation_successes=sum(expe["num_observation_success"] for expe in expset["experiments"]),
        answer_length=sum(expe["dataset"]["size"] for expe in expset["experiments"]),
        observation_length=sum(expe["dataset"]["size"]*expe["num_metrics"] for expe in expset["experiments"]),
    )  # fmt: skip

    # Running status
    if all(expe["experiment_status"] == "pending" for expe in expset["experiments"]):
        status = status_codes["pending"]
    elif all(expe["experiment_status"] == "finished" for expe in expset["experiments"]):
        status = status_codes["finished"]
    else:
        status = status_codes["running"]

    return status, counts


def _get_experiment_data(exp_id):
    """
    for each exp_id, returns query, answer true, answer llm and metrics
    """
    expe = _fetch(
        "get",
        f"/experiment/{exp_id}",
        {"with_dataset": True, "with_results": True},
        refresh=st.session_state.get("refresh_experimentset"),
    )
    if not expe:
        return None

    df = pd.read_json(StringIO(expe["dataset"]["df"]))

    if len(df) == 0 and expe["dataset"]["parquet_size"]:
        if expe["dataset"]["parquet_size"] > 0:
            df = pd.DataFrame(index=range(100))

    # Merge answers and metrics into the dataset dataframe
    if "answers" in expe:
        answers = {answer["num_line"]: answer["answer"] for answer in expe["answers"]}
        errors = {answer["num_line"]: answer["error_msg"] for answer in expe["answers"]}
        df["answer"] = df.index.map(answers)
        if any(error is not None for error in errors.values()):
            df["answer_errors"] = df.index.map(errors)

    if "results" in expe:
        for result in expe["results"]:
            metric_name = result["metric_name"]
            observations = {obs["num_line"]: obs["score"] for obs in result["observation_table"]}
            df[f"result_{metric_name}"] = df.index.map(observations)

    return df


def display_experiment_sets(experiment_sets):
    """
    returns the list of experiments set, with their status/info
    """
    cols = st.columns(3)

    for idx, exp_set in enumerate(experiment_sets):
        status, counts = _get_expset_status(exp_set)

        # Failure status
        has_failure = False
        if counts["total_observation_tries"] > counts["total_observation_successes"]:
            has_failure = True

        status_description = status["text"]
        status_color = status["color"]
        if has_failure:
            status_description += " with some failure"
            status_color = f"linear-gradient(to right, {status_color} 50%, red 50%)"

        when = datetime.fromisoformat(exp_set["created_at"]).strftime("%d %B %Y")
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(
                    f"<div style='position: absolute; top: 10px; right: 10px; "
                    f"width: 10px; height: 10px; border-radius: 50%; "
                    f"background: {status_color};' "
                    f"title='{status_description}'></div>",
                    unsafe_allow_html=True,
                )

                if st.button(f"{exp_set['name']}", key=f"pick_expe_{idx}"):
                    st.query_params["expset"] = exp_set["id"]
                    st.rerun()

                st.markdown(exp_set.get("readme", "No description available"))

                col1, col2, col3 = st.columns([1 / 6, 2 / 6, 3 / 6])
                with col1:
                    st.caption(f"id: {exp_set['id']} ")
                with col2:
                    st.caption(f"Experiments: {len(exp_set['experiments'])} ")
                with col3:
                    st.caption(f"Created the {when}")

    # Show orphan experiments
    # --
    st.markdown("---")
    with st.container(border=True):
        st.markdown(
            f"<div style='position: absolute; top: 10px; right: 10px; "
            f"width: 10px; height: 10px; border-radius: 50%; "
            f"background: {status_color};' "
            f"title='{status_description}'></div>",
            unsafe_allow_html=True,
        )

        if st.button("Orphan experiments", key="pick_expe_orphan"):
            st.query_params["expset"] = "orphan"
            st.rerun()

        st.markdown("The experiments that are not in evaluation sets.")


def display_experiment_set_overview(experimentset, experiments_df):
    """
    returns a dataframe with the list of Experiments and the associated status
    """
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


def display_experiment_details(experimentset, experiments_df):
    experiment_ids = experiments_df["Id"].tolist()
    selected_exp_id = st.selectbox("Select Experiment ID", experiment_ids)
    experiment = next(
        (expe for expe in experimentset.get("experiments", []) if expe["id"] == selected_exp_id),
        None,
    )
    if experiment:
        full_df = _get_experiment_data(experiment["id"])

        if full_df is not None:
            st.write(f"**experiment_id** n° {selected_exp_id}")
            st.write(f"**Name:** {experiment['name']}")
            st.write(f"**Readme:** {experiment['readme']}")

            cols = st.columns(2)
            with cols[0]:
                st.write(f"**Dataset:** {experiment['dataset']['name']}")
                st.write(f"**Judge model:** {experiment['judge_model']}")
            with cols[1]:
                model_name = experiment.get("model") or "Undefined Model"
                st.write(f"**Model:** {model_name}")

            st.dataframe(
                full_df,
                use_container_width=True,
                hide_index=False,
                column_config={"Id": st.column_config.TextColumn(width="small")},
            )
        else:
            st.error("Failed to fetch experiment data")


def _find_default_sort_metric(columns):
    """
    find a sensible default metric for sorting results.
    """
    preferred_metrics = ["judge_precision", "judge_notator", "answer_relevancy", "judge_exactness"]
    for metric in preferred_metrics:
        if metric in columns:
            return f"{metric}"

    return list(columns)[0] if len(columns) > 0 else None


def _extract_mean(value):
    try:
        return float(value.split("±")[0].strip())
    except:
        return value  # Return original value if not in expected format


def _sort_score_df(*dfs, reset_index=False):
    if len(dfs) == 0:
        return

    df = dfs[0]
    sorting_metric = _find_default_sort_metric(df.columns)
    df.sort_values(
        by=sorting_metric,
        key=lambda x: x.map(_extract_mean),
        ascending=False,
        inplace=True,
    )
    # Store the sorted index before resetting it
    sorted_idx = df.index.copy()
    for df in dfs:
        # Reorder df2 inplace to match df1's order
        df.loc[:] = df.loc[sorted_idx].values
        if reset_index:
            # Reset indices inplace
            df.reset_index(drop=True, inplace=True)


def _sort_columns(df: pd.DataFrame, first_columns: list) -> pd.DataFrame:
    first_columns = []
    new_column_order = sorted(first_columns) + sorted(  # Sort the first group of columns
        [col for col in df.columns if col not in first_columns]
    )  # Sort remaining columns
    return df[new_column_order]


def _check_repeat_mode(experiments: list) -> bool:
    """
    check whether the experiment is related to a repetition
    """
    for expe in experiments:
        name = expe["name"]
        if re.search(r"__\d+$", name):
            return True

    return False


def _format_experiments_score_df(experiments: list, df: pd.DataFrame) -> (bool, pd.DataFrame):
    experiment_ids = [expe["id"] for expe in experiments]
    experiment_names = [expe["name"] for expe in experiments]
    is_repeat_mode = _check_repeat_mode(experiments)
    result = None

    if is_repeat_mode and df["model"].notna().all():
        has_repeat = True
        # Lost repetition trailing code.
        df["model"] = df["model"].str.replace(r"__\d+$", "", regex=True)
        # Group by 'model' and calculate mean and std for all numeric columns
        grouped = df.groupby("model").agg(["mean", "std"]).reset_index()

        # Create a new DataFrame to store the results
        result = pd.DataFrame()
        result["model"] = grouped["model"]

        # Iterate over each column (except 'model') to format mean ± std
        for column in df.columns:
            if column not in ["model"]:
                # Format the score as "mean ± std"
                mean_ = grouped[(column, "mean")].round(2).astype(str)
                std_ = grouped[(column, "std")].round(2).astype(str)
                if all(x is None or x == 0 or np.isnan(x) for x in std_.astype(float)):
                    result[column] = mean_
                else:
                    result[column] = mean_ + " ± " + std_

    if result is None or len(result) == len(df):
        df["Id"] = experiment_ids
        # df["name"] = experiment_names
        df = df[["Id", "model"] + [col for col in df.columns if col not in ["Id", "model"]]]
        has_repeat = False
    else:
        df = result

    return has_repeat, df


def display_experiment_set_score(experimentset, experiments_df):
    """Affiche les scores de l'ensemble d'expériences."""
    experiments = experimentset.get("experiments", [])
    _rename_model_variants(experiments)
    size = experiments[0]["dataset"]["size"]

    available_judges = sorted(
        list(set(expe.get("judge_model") for expe in experiments if expe.get("judge_model")))
    ) or ["No_judge_found"]

    rows = []
    rows_support = []
    for expe in experiments:
        row = {}
        row_support = {}

        # Determine model name
        if expe.get("_model") or expe.get("model"):
            model_name = expe.get("_model") or expe["model"]["aliased_name"] or expe["model"]["name"]
        else:
            model_name = f"Undefined model ({expe['name']})"
        row["model"] = model_name
        row_support["model"] = model_name

        # Aggregate results/scores
        for metric_results in expe.get("results", []):
            metric = metric_results["metric_name"]
            scores = [x["score"] for x in metric_results["observation_table"] if pd.notna(x.get("score"))]
            if scores:
                row[f"{metric}"] = np.mean(scores)
                row_support[f"{metric}_support"] = len(scores)

        rows.append(row)
        rows_support.append(row_support)

    if not rows:
        st.error("No valid experiment results found")
        return

    df = pd.DataFrame(rows)
    df = _sort_columns(df, [])

    if "model" not in df.columns:
        df["model"] = [expe.get("name", "Unknown Model") for expe in experiments]

    try:
        has_repeat, df = _format_experiments_score_df(experiments, df)
    except (ValueError, TypeError) as err:
        st.error("No valid result found, try again later...")
        return

    df_support = pd.DataFrame(rows_support)
    df_support = _sort_columns(df_support, [])
    _, df_support = _format_experiments_score_df(experiments, df_support)

    _sort_score_df(df, df_support)

    # To highlight min/max values in each column
    def highlight_min_max(df):
        # Create an empty DataFrame with the same shape as our original
        highlight_df = pd.DataFrame("", index=df.index, columns=df.columns)

        # For each column, find the min and max values and style them
        for col in df.columns:
            if col in ["id", "Id"]:
                continue

            col_means = df[col].apply(_extract_mean)
            if col_means.dtype in [np.float64, np.int64]:
                max_idx = col_means.idxmax()
                min_idx = col_means.idxmin()
                highlight_df.loc[max_idx, col] = "font-weight: bold; color: green"
                highlight_df.loc[min_idx, col] = "font-weight: bold; color: red"

        return highlight_df

    # Show
    # --
    col1, col2 = st.columns([6, 2])
    with col1:
        text = "**Score:** Averaged score on experiments metrics"
        if has_repeat:
            text += ' <em style="font-size:0.85rem;">(aggregated on model repetition)</em>'
        st.markdown(text, unsafe_allow_html=True)
    with col2:
        st.write(f"**Judge model:** {available_judges[0] if available_judges else 'No judge found'}")

    if len(available_judges) > 1:
        st.warning(f"Multiple judge models found: {', '.join(available_judges)}")

    float_columns = df.select_dtypes(include=["float"]).columns
    st.dataframe(
        # Apply styling
        df.style.apply(highlight_min_max, axis=None).format("{:.2f}", subset=float_columns),
        use_container_width=True,
        hide_index=True,
        column_config={"Id": st.column_config.TextColumn(width="small")},
    )

    st.write("---")
    st.write(f"**Support:** the numbers of item on wich the metrics is computed (total items = {size})")
    st.dataframe(
        df_support,
        use_container_width=True,
        hide_index=True,
        column_config={"Id": st.column_config.TextColumn(width="small")},
    )


def count_unique_models_and_metrics(exp_set: dict[str, any]) -> tuple[int, int]:
    unique_models: set[str] = set()
    unique_metrics: set[str] = set()

    experiments = exp_set.get("experiments", [])
    for experiment in experiments:
        model = experiment.get("model", {})
        if "name" in model:
            unique_models.add(model["name"])

        for result in experiment.get("results", []):
            metric_name = result.get("metric_name")
            if metric_name:
                unique_metrics.add(metric_name)

    return len(unique_models), len(unique_metrics)


def convert_range_to_value(value_or_range):
    if isinstance(value_or_range, dict) and "min" in value_or_range and "max" in value_or_range:
        return (value_or_range["min"] + value_or_range["max"]) / 2
    else:
        return value_or_range


def compute_mean_impact(exp_set: dict, impact_key: str):
    total = 0.0
    count = 0
    for experiment in exp_set.get("experiments", []):
        for answer in experiment.get("answers", []):
            emission = answer.get("emission_carbon")
            if not isinstance(emission, dict):
                continue
            impact = emission.get(impact_key, {})
            value = impact.get("value")
            if value is not None:
                total += convert_range_to_value(value)
                count += 1
    if count == 0:
        return None
    return total


st.markdown(
    """
    <style>
    .metric-label {
        font-weight: bold !important;
        font-size: 1.8em !important;
        color: #741b85;
        text-align: center;
        margin-bottom: 0.1em;
    }
    .metric-value {
        font-weight: normal !important;
        font-size: 1.4em !important;
        color: #333333;
        text-align: center;
        margin-top: 0;
    }
    .metric-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 0.4em 0;
    }
    </style>
""",
    unsafe_allow_html=True,
)


def metric_display(label, value):
    return f"""
    <div class="metric-container">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """


def report_ops_global(exp_set):
    st.subheader("🛰️ Global")
    n_models, n_metrics = count_unique_models_and_metrics(exp_set)

    energy_total = compute_mean_impact(exp_set, "energy")
    gwp_total = compute_mean_impact(exp_set, "gwp")
    energy_str = f"{energy_total:.3f} kWh" if energy_total is not None else "NR"
    if gwp_total is None:
        carbon_str = "NR"
    elif gwp_total < 1:
        carbon_str = f"{gwp_total*1000:.1f} gCO₂eq"
    else:
        carbon_str = f"{gwp_total:.3f} kgCO₂eq"

    cols = st.columns(4)
    for col, (label, value) in zip(
        cols,
        [("Models", n_models), ("Metrics", n_metrics), ("Energy", energy_str), ("GHG Emissions", carbon_str)],
    ):
        col.markdown(metric_display(label, value), unsafe_allow_html=True)

    st.subheader("🧭 Status by Experiment Set")

    report_data = []
    if exp_set:
        status, counts = _get_expset_status(exp_set)

        has_failure = counts["total_observation_tries"] > counts["total_observation_successes"]
        if has_failure:
            with st.expander("Failure Analysis", expanded=False):
                for expe in exp_set["experiments"]:
                    if expe["num_try"] != expe["num_success"]:
                        st.write(f"id: {expe['id']} name: {expe['name']} (failed on output generation)")
                        continue

                    if expe["num_observation_try"] != expe["num_observation_success"]:
                        st.write(f"id: {expe['id']} name: {expe['name']} (failed on score computation)")
                        continue

        report_data.append(
            {
                "Experiment Set Name": exp_set["name"],
                "Status": status["text"],
                "Total Experiments": len(exp_set["experiments"]),
                "Answer Tries": counts["total_answer_tries"],
                "Answer Successes": counts["total_answer_successes"],
                "Observation Tries": counts["total_observation_tries"],
                "Observation Successes": counts["total_observation_successes"],
                "Has Failure": has_failure,
            }
        )

    report_df = pd.DataFrame(report_data)
    st.dataframe(
        report_df,
        use_container_width=True,
        hide_index=True,
    )


def compute_failure_rates(exp_set: dict[str, any]) -> tuple[dict[str, float], dict[str, float]]:
    model_stats = defaultdict(lambda: {"num_try": 0, "num_success": 0})
    metric_stats = defaultdict(lambda: {"num_try": 0, "num_success": 0})

    experiments = exp_set.get("experiments", [])

    for experiment in experiments:
        model = experiment.get("model", {})
        model_name = model.get("name")
        num_try = experiment.get("num_try", 0)
        num_success = experiment.get("num_success", 0)
        if model_name:
            model_stats[model_name]["num_try"] += num_try
            model_stats[model_name]["num_success"] += num_success

        for result in experiment.get("results", []):
            metric_name = result.get("metric_name")
            r_num_try = result.get("num_try", 0)
            r_num_success = result.get("num_success", 0)
            if metric_name:
                metric_stats[metric_name]["num_try"] += r_num_try
                metric_stats[metric_name]["num_success"] += r_num_success

    model_failure_rate = {
        name: 1 - (stats["num_success"] / stats["num_try"]) if stats["num_try"] > 0 else 0.0
        for name, stats in model_stats.items()
    }
    metric_failure_rate = {
        name: 1 - (stats["num_success"] / stats["num_try"]) if stats["num_try"] > 0 else 0.0
        for name, stats in metric_stats.items()
    }

    return model_failure_rate, metric_failure_rate


def display_failure_analysis(exp_set: dict) -> None:
    st.subheader("🚨 Failure rate analysis")

    model_failure, metric_failure = compute_failure_rates(exp_set)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🤖 By model")
        if not model_failure or all(v == 0 for v in model_failure.values()):
            st.info("No models with failure")
        else:
            for model, rate in sorted(model_failure.items(), key=lambda x: -x[1]):
                st.markdown(f"**{model}**")
                st.progress(rate, text=f"{rate:.1%} failures")
                st.write("---")

    with col2:
        st.subheader("📏 By metric")
        if not metric_failure or all(v == 0 for v in metric_failure.values()):
            st.info("No metrics with failure")
        else:
            for metric, rate in sorted(metric_failure.items(), key=lambda x: -x[1]):
                st.markdown(f"**{metric}**")
                st.progress(rate, text=f"{rate:.1%} failures")
                st.write("---")


def display_ops_analysis(experimentset):
    report_ops_global(experimentset)
    display_failure_analysis(experimentset)


def show_header(experimentset):
    status, counts = _get_expset_status(experimentset)
    st.markdown(f"## {experimentset['name']}")
    col1, col2 = st.columns([1 / 12, 1])
    with col1:
        st.markdown(f"**Id**: {experimentset['id']}")
    with col2:
        try:
            when = datetime.fromisoformat(experimentset["created_at"]).strftime("%d %B %Y")
        except ValueError:
            when = "N/A"
        st.caption(f"Created the {when}")
    st.markdown(f"**Readme:** {experimentset.get('readme', 'No description available')}")

    finished_ratio = 0
    failure_ratio = 0
    if counts["observation_length"] > 0:
        finished_ratio = int(counts["total_observation_successes"] / counts["observation_length"] * 100)
        failure_ratio = int(
            (counts["total_observation_tries"] - counts["total_observation_successes"])
            / counts["observation_length"]
            * 100
        )

    run_status = f"**Finished**: {finished_ratio}%"
    if failure_ratio > 0:
        run_status += f" &nbsp;&nbsp;&nbsp; Failure: <span style='color:red;'>{failure_ratio}%</span>"

    st.markdown(run_status, unsafe_allow_html=True)


def main():
    # Fetch or re-fetch data
    # --
    experiment_sets = _fetch("get", "/experiment_sets", refresh=st.session_state.get("refresh_main"))

    # View Branching
    # --
    expid = st.query_params.get("expset") or st.session_state.get("expset_id")
    if expid:
        st.session_state["expset_id"] = expid
        st.query_params.expset = expid

        # Get the expset (or the orphan experiments)
        if expid.isdigit():
            experimentset = next((x for x in experiment_sets if x["id"] == int(expid)), None)
            experimentset = _fetch_experimentset(
                expid,
                experimentset,
                refresh=st.session_state.get("refresh_experimentset"),
                with_eco=False,
            )
        elif expid == "orphan":
            experimentset = {
                "id": None,
                "name": "Orphan experiments",
                "created_at": "",
                "experiments": fetch("get", "/experiments", {"orphan": True, "backward": True}),
            }

        else:
            st.error("Invalid experiment set id: %s" % expid)
            return

        # Horizontal menu toolbar
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(":arrow_left: Go back", key="go_back"):
                st.session_state["expset_id"] = None
                st.query_params.pop("expset")
                st.rerun()

        with col2:
            if st.button("🔄 Refresh", key="refresh_experimentset"):
                st.rerun()

        experiments_df = pd.DataFrame(
            [
                {
                    "Id": expe["id"],
                    "Name": expe["name"],
                    "Dataset": expe["dataset"]["name"],
                    "Model": (expe["model"]["aliased_name"] or expe["model"]["name"])
                    if expe.get("model")
                    else "Undefined model",
                    "Model params": _format_model_params(expe),
                    "Status": expe["experiment_status"],
                    "Created at": expe["created_at"],
                    "Num try": expe["num_try"],
                    "Num success": expe["num_success"],
                    "Num observation try": expe["num_observation_try"],
                    "Num observation success": expe["num_observation_success"],
                }
                for expe in experimentset["experiments"]
            ]
        )
        experiments_df.sort_values(by="Id", ascending=True, inplace=True)

        show_header(experimentset)

        # Display tabs
        # --
        tab_index = {
            1: {
                "key": "scores",
                "title": "⭐ Scores",
                "func": display_experiment_set_score,
            },
            2: {
                "key": "overview",
                "title": "📊 Set Overview",
                "func": display_experiment_set_overview,
            },
            3: {
                "key": "details",
                "title": "📝 Details by Experiment Id",
                "func": display_experiment_details,
            },
            4: {
                "key": "ops",
                "title": "🚨 Ops Analysis",
                "func": display_ops_analysis,
            },
        }
        tab_reverse = {d["key"]: k for k, d in tab_index.items()}
        # @TODO: how to catch the tab click in order to set the current url query to tab key ?

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                tab_index[1]["title"],
                tab_index[2]["title"],
                tab_index[3]["title"],
                tab_index[4]["title"],
            ]
        )

        def show_warning_in_tabs(message):
            with tab1:
                st.warning(message)
            with tab2:
                st.warning(message)
            with tab3:
                st.warning(message)

        df = experiments_df  # alias
        if not (df["Status"] == "finished").all():
            show_warning_in_tabs("Warning: some experiments are not finished.")
        if df["Num success"].sum() != df["Num try"].sum():
            show_warning_in_tabs("Warning: some answers are failed.")
        if df["Num observation success"].sum() != df["Num observation try"].sum():
            show_warning_in_tabs("Warning: some metrics are failed.")

        with tab1:
            tab_index[1]["func"](experimentset, experiments_df)
        with tab2:
            tab_index[2]["func"](experimentset, experiments_df)
        with tab3:
            tab_index[3]["func"](experimentset, experiments_df)
        with tab4:  # TODO : see how pass this fetch in this condition : 'if expid.isdigit():'
            experimentset_ops = _fetch_experimentset(
                expid,
                next((x for x in experiment_sets if x["id"] == int(expid)), None),
                refresh=st.session_state.get("refresh_experimentset"),
                with_eco=True,
            )
            tab_index[4]["func"](experimentset_ops)

    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.title("Experiments")
        with col2:
            if st.button("🔄 Refresh", key="refresh_main"):
                st.rerun()

        display_experiment_sets(experiment_sets)


main()
