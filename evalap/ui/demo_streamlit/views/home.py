import os
from PIL import Image
import streamlit as st
from routes import ROUTES
from pathlib import Path
# from streamlit_card import card


def get_logo(filename="evalap_logo.png"):
    img_path = Path(__file__).resolve().parents[1] / "static" / "images"
    logo_path = img_path / filename
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
    else:
        logo = Image.new("RGBA", (200, 100), (255, 255, 255, 0))
    return logo


col1, col2, _ = st.columns([0.2, 0.6, 0.2])  # Image column is 20%, content column is 80%

with col1:
    st.image(get_logo(), width=150)

with col2:
    st.title("Welcome to EvalAP")

st.markdown(
    """
<style>
    /* Increase font size for page links */
    .stPageLink {
        margin-bottom: 12px !important; /* Add more space between items */
    }

    /* Make the link text bold */
    .stPageLink p {
        font-size: 1.2rem !important;  /* Adjust size as needed */
        font-weight: 500 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

for route in ROUTES:
    if route["id"] in ["home"] or route.get("is_hidden"):
        continue
    st.page_link(route["path"], label=f"{route['title']}: {route['description']}", icon=route["icon"])
    # card(
    #    title= route['title'],
    #    text=route['description'],
    # )


st.markdown("Explore [our documentation](/doc) for more information.")
