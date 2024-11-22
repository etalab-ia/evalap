import streamlit as st
from routes import ROUTES, get_page


pg = st.navigation([get_page(route) for route in ROUTES])
st.set_page_config(layout="wide")
custom_css = """
<style>
* {
    font-size: 18px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


pg.run()
