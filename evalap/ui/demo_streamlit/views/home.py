import os
from pathlib import Path

import streamlit as st
from PIL import Image
from routes import ROUTES

# from streamlit_card import card


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
    st.title("Bienvenue sur EvalAP")

st.write("") # add a small vertical space

col1, col2 = st.columns([0.5, 0.5])
with col1:
    for route in ROUTES:
        if route["id"] in ["home"] or route.get("is_hidden"):
            continue
        st.page_link(route["path"], label=f"{route['title']}: {route['description']}", icon=route["icon"])
        # card(
        #    title= route['title'],
        #    text=route['description'],
        # )




with col2:
    st.markdown(
        """
        <style>
        /* DSFR Blue and styling for Notions Clefs box */
        .custom-info-box {
            border: 2px solid #2323FF; /* Bleu DSFR */
            padding: 1rem 1.5rem;
            border-radius: 8px;
            background-color: #f0f4ff; /* Fond bleu clair */
            margin-bottom: 20px;
            font-family: Arial, sans-serif;
            color: #000;
        }
        .custom-info-box h3 {
            color: #2323FF; /* Bleu DSFR */
            font-weight: 700;
            margin-bottom: 10px;
            font-size: 1.3rem;
        }

        /* Style for page links */
        .stPageLink {
            margin-bottom: 12px !important;
        }
        /* Make the link text larger and semi-bold */
        .stPageLink p {
            font-size: 1.2rem !important;
            font-weight: 500 !important;
        }
        </style>

        <div class="custom-info-box">
            <h3>Key Concepts</h3>
            <ul>
                <li><b>EvalAP</b> operates using the <em>Experiment Set</em> logic.</li>
                <li>An <em>Experiment Set</em> groups multiple experiments related for a given evaluation run. For example:
                    <ul>
                        <li>Finding the best system prompt for your use case.</li>
                        <li>Finding the best parametrization of a RAG engine.</li>
                        <li>Finding bias or regression in a set of models.</li>
                    </ul>
                </li>
                <li>To run an experiment (set), you need:
                    <ol>
                        <li>A dataset - either import your own or choose from available datasets.</li>
                        <li>One or several metrics - a metric will guide your decision-making.</li>
                        <li>AI models/systems you want to evaluate.</li>
                    </ol>
                </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    st.markdown("Explore [our documentation](/doc) for more information.")
