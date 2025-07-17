import os
from PIL import Image
import streamlit as st
from routes import ROUTES
from pathlib import Path


def get_logo(filename="evalap_logo.png"):
    img_path = Path(__file__).resolve().parents[1] / "static" / "images"
    logo_path = img_path / filename
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
    else:
        logo = Image.new("RGBA", (200, 100), (255, 255, 255, 0))
    return logo


col1, col2 = st.columns([4, 2])

with col1:
    st.title("Welcome to EvalAP")
    st.write("What is on the menu :")
    for route in ROUTES:
        if route["id"] in ["home"] or route.get("is_hidden"):
            continue
        st.page_link(route["path"], label=f"{route['title']}: {route['description']}", icon=route["icon"])

with col2:
    st.image(get_logo(), use_container_width=True)
