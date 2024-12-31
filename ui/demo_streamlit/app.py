import streamlit as st
from routes import ROUTES, get_page
from utils import load_css

# Configuration 
st.set_page_config(
    page_title="EG1 - Évaluation",
    page_icon="ui/demo_streamlit/static/images/eg1_logo.png", 
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css("style.css")

pg = st.navigation([get_page(route) for route in ROUTES])

pg.run()
