import streamlit as st
from routes import ROUTES
from PIL import Image

logo_path = "evalap/ui/demo_streamlit/static/images/EvalAP_logo.png"  
logo = Image.open(logo_path)

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
