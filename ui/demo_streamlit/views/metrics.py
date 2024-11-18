import streamlit as st
from utils import fetch

from streamlit import session_state

session_state.layout = "wide"


def main():
    st.title("Metrics")

    metrics = fetch("get", "/metrics")
    if not metrics:
        return

    main_content, right_menu = st.columns([8, 2])

    # Main content
    with main_content:
        with st.container():
            st.write("""A metric is a quantitative measure applied to an observation of a model's output.
                     Each metric has a specified "require" constraint that indicates which column in the dataset is needed to perform the measurement.
                     The metric returns a score (float) and may optionally include an observation, which is the intermediate result (such as a judge string output).
                    """)

        for metric in metrics:
            with st.container():
                # Add an anchor for navigation
                st.markdown(
                    f"<div id='{metric['name'].lower().replace(' ', '-')}'></div>",
                    unsafe_allow_html=True,
                )
                st.subheader(metric["name"])
                st.write(
                    f"Required fields: {', '.join(map(lambda x: '**' + x + '**', metric['require']))}"
                )
                st.write(metric["description"])
                st.divider()

    # Navigation menu
    with right_menu:
        st.markdown("###### Quick Navigation")
        for metric in metrics:
            metric_id = metric["name"].lower().replace(" ", "-")
            st.markdown(
                f"""
                <a href="#{metric_id}" style="color:grey;"
                   onclick="document.getElementById('{metric_id}').scrollIntoView({{behavior: 'smooth'}});">
                    {metric['name']}
                </a><br>
            """,
                unsafe_allow_html=True,
            )


main()
