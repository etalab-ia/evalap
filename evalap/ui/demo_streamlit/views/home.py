import os
from PIL import Image
import streamlit as st
from routes import ROUTES

def get_logo_path(filename="evalap_logo.png"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, '..', 'static', 'images', filename)
    return os.path.normpath(logo_path)

logo_path = get_logo_path()  # Tu peux adapter le nom si besoin

if os.path.exists(logo_path):
    logo = Image.open(logo_path)
else:
    logo = Image.new("RGBA", (200, 100), (255, 255, 255, 0))  

col1, col2 = st.columns([4, 2])

with col1:
    st.title("Welcome to EvalAP")
    st.write("What is on the menu :")
    for route in ROUTES:
        if route["id"] in ["home"] or route.get("is_hidden"):
            continue
        st.page_link(
            route["path"],
            label=f'{route["title"]}: {route["description"]}',
            icon=route["icon"]
        )

with col2:
    st.image(logo, use_container_width=True)
