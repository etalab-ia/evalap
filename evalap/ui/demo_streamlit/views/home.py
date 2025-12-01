import os
from pathlib import Path

import streamlit as st
from PIL import Image

# ---------- Header ----------


def get_logo(filename="evalap_logo.png"):
    img_path = Path(__file__).resolve().parents[1] / "static" / "images"
    logo_path = img_path / filename
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
    else:
        logo = Image.New("RGBA", (200, 100), (255, 255, 255, 0))
    return logo


col1, col2, _ = st.columns([0.2, 0.6, 0.2])  # Image column is 20%, content column is 60%

with col1:
    st.image(get_logo(), width=150)

with col2:
    st.title("EvalAP")

# ---------- Content ----------
st.write(
    "EvalAP supports you in the **development** and **pre‑production evaluation** "
    "of AI systems, primarily systems that include RAG."
)

st.write(
    """EvalAP is built around the concept of experiment sets.

An experiment set groups several related experiments for a given evaluation:

- Find the system that best fits your business use case
- Find the best configuration of a RAG engine
- Detect biases or regressions in a set of models

To run an experiment, you need:

- A test dataset
- One or more metrics and a judge
- The AI models/systems to evaluate, or question–answer pairs to evaluate
"""
)

st.markdown(
    '<h2 style="font-size: 20px; font-weight: bold; margin-top: 1.5rem; margin-bottom: 1rem;">Start your evaluation with our guides:</h2>',
    unsafe_allow_html=True,
)


# ---------- Cards ----------
cols = st.columns(4)

DOC_URL = "https://evalap.etalab.gouv.fr/doc/"
NB_URL = "https://github.com/etalab-ia/evalap/blob/main/notebooks/"

cards = [
    (
        "Publish a dataset",
        DOC_URL + "fr/docs/user-guides/add-your-dataset",
        NB_URL + "run_evals_for_your_own_IA_system.ipynb",
    ),
    (
        "Configure metrics",
        DOC_URL + "fr/docs/developer-guide/adding-a-new-metric",
        NB_URL + "run_judge_adhoc.ipynb",
    ),
    (
        "Run an experiment",
        DOC_URL + "fr/docs/user-guides/evaluate-your-own-ia-system#22-run-eval",
        NB_URL + "run_evals_for_your_own_IA_system.ipynb",
    ),
    (
        "Run a compliance experiment",
        DOC_URL + "fr/docs/user-guides/create-compliance-experiment#define-your-compliance-experiment",
        NB_URL + "run_compliance.ipynb",
    ),
]

st.markdown(
    """
    <style>
    div[data-testid="stVerticalBlock"] > div:has(div.evalap-card) div[data-testid="stLinkButton"] {
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

for col, (title, doc_link, nb_link) in zip(cols, cards):
    with col:
        with st.container(border=True):
            st.markdown('<div class="evalap-card">', unsafe_allow_html=True)
            st.markdown(
                f'<h3 style="text-align: center; font-size: 1.1rem; margin-bottom: 0.25rem;">{title}</h3>',
                unsafe_allow_html=True,
            )
            st.link_button("Documentation", doc_link)
            st.link_button("Notebook", nb_link)
            st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    "Explore the [documentation](https://evalap.etalab.gouv.fr/doc/) and [notebook](https://github.com/etalab-ia/evalap/blob/main/notebooks/)"
)
