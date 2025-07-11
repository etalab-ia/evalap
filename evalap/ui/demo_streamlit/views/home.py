import streamlit as st
from routes import ROUTES

st.title("Welcome to EvalAP")


st.write("What is on the menu:")

for route in ROUTES:
    if route["id"] in ["home"] or route.get("is_hidden"):
        continue

    st.page_link(
        route["path"], label=f'{route["title"]}: {route["description"]}', icon=route["icon"]
    )
