import streamlit as st
from routes import ROUTES, get_page

st.set_page_config(
    page_title="EvalAP - Évaluation API and Platform",
    page_icon="evalap/ui/demo_streamlit/static/images/evalap_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

#
# Customize base style
#
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

