import re
from itertools import groupby
from operator import itemgetter

import streamlit as st
from streamlit import session_state
from utils import fetch

session_state.layout = "wide"


def extract_template_variable(py_file):
    try:
        with open(py_file, "r", encoding="utf-8") as f:
            content = f.read()
        result = re.search(r'_template\s*=\s*([\'"]{3})([\s\S]*?)\1', content, re.DOTALL)
        return result.group(2).strip() if result else "**Definition not found in file.**"
    except FileNotFoundError:
        return "**Files not found :  {}**".format(py_file)


def main():
    st.title("Metrics")

    metrics = fetch("get", "/metrics")
    if not metrics:
        return

    main_content, right_menu = st.columns([8, 2])

    # Group metrics by type
    sorted_metrics = sorted(metrics, key=itemgetter("type"))
    grouped_metrics = {k: list(v) for k, v in groupby(sorted_metrics, key=itemgetter("type"))}

    # Main content
    with main_content:
        with st.container():
            st.write("""A metric is a quantitative measure applied to an observation of a model's output.
                     Each metric has a specified "require" constraint that indicates which column in the dataset is needed to perform the measurement.
                     The metric returns a score (float) and may optionally include an observation, which is the intermediate result (such as a judge string output).
                    """)

        for metric_type, metrics_group in grouped_metrics.items():
            # Add an anchor for each metric type
            st.markdown(f"<div id='{metric_type.lower()}'></div>", unsafe_allow_html=True)
            st.header(f"{metric_type.capitalize()} Metrics")
            for metric in metrics_group:
                with st.container():
                    st.markdown(
                        f"<div id='{metric['name'].lower().replace(' ', '-')}'></div>",
                        unsafe_allow_html=True,
                    )
                    st.subheader(metric["name"])
                    st.write(
                        f"Required fields: {', '.join(map(lambda x: '**' + x + '**', metric['require']))}"
                    )
                    st.write(metric["description"])

                    # pop up for definition
                    if metric["name"].startswith("judge_"):
                        definition = extract_template_variable(f"evalap/api/metrics/{metric['name']}.py")
                        with st.popover("Show me the prompt"):
                            st.markdown(definition, unsafe_allow_html=True)

                    st.divider()

    # Navigation menu
    with right_menu:
        st.markdown("###### Quick Navigation")
        for metric_type, metrics_group in grouped_metrics.items():
            metric_type_id = metric_type.lower()

            # Create a button for each metric type
            st.markdown(
                f"""
                <a href="#{metric_type_id}" style="color:grey; font-weight:bold;"
                   onclick="document.getElementById('{metric_type_id}').scrollIntoView({{behavior: 'smooth'}});">
                    {metric_type.capitalize()} metrics
                </a><br>
            """,
                unsafe_allow_html=True,
            )

            # Add clickable links for each metric under its type
            for metric in metrics_group:
                metric_id = metric["name"].lower().replace(" ", "-")
                st.markdown(
                    f"""
                    <a href="#{metric_id}" style="color:grey; margin-left:15px;"
                       onclick="document.getElementById('{metric_id}').scrollIntoView({{behavior: 'smooth'}});">
                        {metric["name"]}
                    </a><br>
                """,
                    unsafe_allow_html=True,
                )


main()
