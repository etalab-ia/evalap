import streamlit as st

from views.test_standard_evaluation import render_launch_tab
from views.test_your_own_evaluation import render_test_tab


def init_page_styles():
    st.markdown(
        """
        <style>
        h3 {
            font-size: 20px !important;
            font-weight: 600;
        }
        .custom-button {
            background-color: transparent;
            color: #000091;
            border: 2px solid #000091;
            padding: 12px 28px;
            font-size: 20px;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            text-align: center;
            text-decoration: none;
            display: inline-block;
        }
        .custom-button:hover {
            background-color: #000091;
            color: white;
            border-color: #000091;
        }
        /* Style des onglets */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px;
            font-size: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def info_banner(text):
    """Display info banner with custom styling"""
    st.markdown(
        f"""
        <div style="
            background-color:#E3ECFF;
            color:#000091;
            border:1px solid #B5C7F9;
            padding:18px;
            border-radius:7px;
            margin-bottom:24px;
            ">
            <span style="font-size:20px; font-weight:normal;">
                {text}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
