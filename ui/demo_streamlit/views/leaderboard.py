import pandas as pd
import streamlit as st
from utils import fetch
import requests

API_URL = "http://localhost:8000/v1"

@st.cache_data(ttl=600)
def fetch_leaderboard_():
    endpoint = "/leaderboard"
    return fetch("get", endpoint)

def main():
    st.title("EG1 Leaderboard ")
    st.write("## 🏆 Top Performing LLMs Leaderboard")
    st.write("")

    leaderboard_data = fetch_leaderboard_()

    if leaderboard_data and leaderboard_data["entries"]:
        df = pd.DataFrame([
            {
                "Model": entry["model_name"],
                "Dataset": entry["dataset_name"],
                "Judge Notator Score": entry["judge_notator_score"],
                **entry["other_metrics"]
            }
            for entry in leaderboard_data["entries"]
        ])

        st.dataframe(
            df.sort_values("Judge Notator Score", ascending=False, na_position='last'),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.write("No data available for the leaderboard.")

main()
