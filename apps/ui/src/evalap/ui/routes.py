import streamlit as st

ROUTES = [
    {
        "id": "home",
        "path": "views/home.py",
        "title": "Home",
        "icon": ":material/home:",
    },
    # {
    #     "id": "leaderboard",
    #     "path": "views/leaderboard.py",
    #     "title": "Leaderboard",
    #     "description": "Best models ranking list",
    #     "icon": ":material/trophy:",
    # },
    {
        "id": "leaderboard",
        "path": "views/product_leaderboard.py",
        "title": "Leaderboard",
        "description": "Best models ranking list (by products)",
        "icon": ":material/trophy:",
    },
    {
        "id": "prompt_analyze",
        "path": "views/prompt_analyze.py",
        "title": "Prompt analyze",
        "description": "Analyze differents prompts for your product",
        "icon": ":material/trophy:",
    },
    {
        "id": "experiments_set",
        "path": "views/experiments_set.py",
        "title": "Experiments",
        "description": "Navigate the experiments collections groups",
        "icon": ":material/experiment:",
    },
    {
        "id": "compliance",
        "path": "views/compliance.py",
        "title": "Compliance",
        "description": "AI system compliance",
        "icon": ":material/fact_check:",
    },
    {
        "id": "launch",
        "path": "views/launch_test_evaluation.py",
        "title": "Test EvalAP",
        "description": "Test an evaluation",
        "icon": ":material/rocket_launch:",
    },
    {
        "id": "datasets",
        "path": "views/datasets.py",
        "title": "Datasets",
        "description": "A list of available datasets",
        "icon": ":material/database:",
    },
    {
        "id": "metrics",
        "path": "views/metrics.py",
        "title": "Metrics",
        "description": "A list of available metrics",
        "icon": ":material/visibility:",
    },
    {
        "id": "ops",
        "path": "views/ops.py",
        "title": "Usage statistics",
        "description": "Statistical overview of usage",
        "icon": ":material/settings:",
    },
]


def get_page(route: str | dict):
    if isinstance(route, str):
        route = next((x for x in ROUTES if x["id"] == route), None)
    elif isinstance(route, dict):
        pass
    else:
        raise ValueError("Unsupported data type for route: %s" % type(route))

    if route is None:
        raise ValueError("Route not found: %s" % route)

    page = st.Page(route["path"], title=route["title"], icon=route.get("icon"), url_path=route["id"])
    return page
