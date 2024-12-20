import pandas as pd
import streamlit as st
from utils import fetch


@st.cache_data(ttl=600)
def fetch_leaderboard(metric_name="judge_notator", limit=30):
    endpoint = "/leaderboard"
    params = {"metric_name": metric_name, "limit": limit}
    return fetch("get", endpoint, params)

def main():
    st.title("EG1 Leaderboard")
    
    metric_name = "judge_notator"
    limit = 30
    
    st.write(f"## 🏆 Top Performing LLMs Leaderboard - {metric_name.replace('_', ' ').title()}")
    st.write("")

    leaderboard_data = fetch_leaderboard(metric_name, limit)

    if leaderboard_data and leaderboard_data["entries"]:
        df = pd.DataFrame([
            {
                "Model": entry["model_name"],
                "Dataset": entry["dataset_name"],
                f"{metric_name.replace('_', ' ').title()} Score": entry["main_metric_score"],
                **entry["other_metrics"]
            }
            for entry in leaderboard_data["entries"]
        ])

        st.dataframe(
            df.sort_values(f"{metric_name.replace('_', ' ').title()} Score", ascending=False, na_position='last'),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.write("No data available for the leaderboard.")

main()
