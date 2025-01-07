import streamlit as st
from routes import ROUTES, get_page

st.set_page_config(
    page_title="EG1 - Évaluation",
    page_icon="ui/demo_streamlit/static/images/eg1_logo.png", 
    layout="wide",
    initial_sidebar_state="expanded",
)

custom_css = """
<style>
body {
    font-size: 18px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

pg = st.navigation([get_page(route) for route in ROUTES])

pg.run()
