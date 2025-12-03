import streamlit as st
from utils import fetch

ROUTES = [
    {
        "id": "home",
        "path": "views/home.py",
        "title": "Home",
        "icon": ":material/home:",
    },
    {
        "id": "metrics",
        "path": "views/metrics.py",
        "title": "Metrics",
        "description": "A list of available metrics",
        "icon": ":material/visibility:",
    },
    {
        "id": "datasets",
        "path": "views/datasets.py",
        "title": "Datasets",
        "description": "A list of available datasets",
        "icon": ":material/database:",
    },
    {
        "id": "experiments_set",
        "path": "views/experiments_set.py",
        "title": "Experiments",
        "description": "Navigate the experiments collections groups",
        "icon": ":material/experiment:",
    },
    {
        "id": "launch",
        "path": "views/launch_test_evaluation.py",
        "title": "Test EvalAP",
        "description": "Test an evaluation",
        "icon": ":material/rocket_launch:",
    },
    {
        "id": "ops",
        "path": "views/ops.py",
        "title": "Usage statistics",
        "description": "Statistical overview of usage",
        "icon": ":material/settings:",
    },
]


def is_db_empty(refresh_needed=False):
    all_experiment_sets = fetch("get", "/experiment_sets", data={}, refresh=refresh_needed)
    return len(all_experiment_sets) == 0


def main():
    db_empty = is_db_empty()

    available_routes = [route for route in ROUTES if not (db_empty and route["id"] == "ops")]

    pages = [
        st.Page(route["path"], title=route["title"], icon=route.get("icon"), url_path=route["id"])
        for route in available_routes
    ]

    page = st.navigation(pages)
    page.run()
