import streamlit as st
from ui_components import info_banner, init_page_styles

from views.test_standard_evaluation import render_launch_tab
from views.test_your_own_evaluation import render_test_tab


def main():
    init_page_styles()

    st.title("Tests evaluations")

    info_banner(
        "ℹ️ This test evaluation runs on a RAG (Retrieval-Augmented Generation) system, "
        "combining document retrieval with LLM reasoning to assess overall performance."
    )

    tab_launch, tab_test = st.tabs(
        ["Run test evaluations with Albert API", "Run your own AI system evaluations"]
    )

    with tab_launch:
        render_launch_tab()

    with tab_test:
        render_test_tab()


main()
