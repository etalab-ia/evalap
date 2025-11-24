import copy
import json
from datetime import datetime

import requests
import streamlit as st
import streamlit.components.v1 as components
from template_manager import TemplateManager
from utils import fetch

# --- Configuration ---

PROMPT_CHOICES = [
    "Summarize the selected decree.",
    "Reply as a front-desk staff member to a frequent question.",
    "Explain the procedure linked to the selected guide.",
]

DEFAULT_MODEL = "albert-small"
DEFAULT_JUDGE_MODEL = "albert-large"
CHOICE_METRICS = ["judge_notator", "judge_exactness"]
DEFAULT_METRICS = [
    "generation_time",
    "nb_tokens_prompt",
    "nb_tokens_completion",
    "energy_consumption",
    "gwp_consumption",
]
DEFAULT_TEMPERATURE = 0.2
DEFAULT_PROVIDER_URL = "https://albert.api.etalab.gouv.fr/v1"
DEFAULT_METHOD_COLLECTION = "semantic"

ALBERT_PROVIDER_URL = DEFAULT_PROVIDER_URL

template_manager = TemplateManager()


# --- Utilitary Functions ---


def info_banner(message):
    st.markdown(
        f"""
        <div style="
            background-color:#E3ECFF;
            color:#000091;
            border:1px solid #B5C7F9;
            padding:18px;
            border-radius:7px;
            margin-bottom:24px;
            ">
        <strong>ℹ️ {message}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )


button_style = """
<style>
.custom-button {
    background-color: transparent;       /* Pas de fond */
    color: #000091;                      /* Texte bleu DSFR */
    border: 2px solid #000091;           /* Contour bleu DSFR */
    padding: 12px 28px;
    font-size: 20px;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
    text-align: center;
    text-decoration: none;
    display: inline-block;
}
.custom-button:hover {
    background-color: #000091;           /* Fond bleu DSFR au survol */
    color: white;                        /* Texte blanc au survol */
    border-color: #000091;
}
</style>
"""


def get_public_collections(api_key):
    url = f"{ALBERT_PROVIDER_URL}/collections"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        public_cols = [
            {"id": collection["id"], "name": collection["name"]}
            for collection in data.get("data", [])
            if collection.get("visibility") == "public"
            and "data-gouv-datasets-catalog" not in collection.get("name", "")
        ]
        return public_cols
    else:
        st.error(f"Error fetching collections: {response.status_code}")
        return []


def _should_skip_dataset(dataset: dict) -> bool:
    return "output" in dataset.get("columns", [])


def list_datasets() -> list[str]:
    datasets = fetch("get", "/datasets")
    if not datasets:
        st.warning("No dataset available")
        return []

    allowed = {"test_service_public", "test_annuaire_entreprises"}

    filtered = [ds["name"] for ds in datasets if ds["name"] in allowed and not _should_skip_dataset(ds)]

    if not filtered:
        st.warning("No datasets available among the filtered datasets.")
    return filtered


def post_experiment_set(expset, token):
    return fetch("post", "/experiment_set", data=expset, token=token)


def create_experiment_set(
    dataset,
    collection_ids,
    model_name,
    prompt,
    judge_model,
    api_key,
    metrics,
):
    model_config = {
        "name": model_name,
        "base_url": DEFAULT_PROVIDER_URL,
        "api_key": api_key,
        "system_prompt": prompt.strip(),
        "sampling_params": {"temperature": DEFAULT_TEMPERATURE},
    }
    if collection_ids:
        model_config["extra_params"] = {
            "search": True,
            "search_args": {
                "method": DEFAULT_METHOD_COLLECTION,
                "collections": collection_ids,
                "k": 10,
            },
        }

    expset_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_launch_test_evaluation"

    expset = {
        "name": expset_name,
        "readme": "Experiment for_launch test",
        "cv": {
            "common_params": {
                "dataset": dataset,
                "metrics": metrics,
                "judge_model": {
                    "name": judge_model,
                    "base_url": DEFAULT_PROVIDER_URL,
                    "api_key": api_key,
                },
            },
            "grid_params": {"model": [model_config]},
            "repeat": 1,
        },
    }

    return expset


def copy_to_clipboard_button(text_to_copy: str, button_id: str = "copy_btn", height: int = 60):
    safe_text = json.dumps(text_to_copy)
    html = f"""
        <button
            id="{button_id}"
            onclick="copyToClipboard(this)"
            style="
                background-color:#4CAF50;
                color:white;
                border:none;
                padding:8px 16px;
                border-radius:8px;
                cursor:pointer;
                margin-top:1rem;
                width:100%;
            ">
            📋 Copy to clipboard
        </button>
        <script>
        function copyToClipboard(button) {{
            const originalText = button.innerHTML;
            const text = {safe_text};
            navigator.clipboard.writeText(text).then(() => {{
                button.innerHTML = "✅ Copied!";
                setTimeout(() => {{
                    button.innerHTML = originalText;
                }}, 3000);
            }}).catch(err => {{
                console.error('Failed to copy: ', err);
                button.innerHTML = "❌ Failed to copy";
                setTimeout(() => {{
                    button.innerHTML = originalText;
                }}, 3000);
            }});
        }}
        </script>
    """
    components.html(html, height=height)


# --- Main page ---


def main():
    st.title("Start an Evaluation with Albert API")

    info_banner("To launch a test evaluation, Albert API access is required")

    # Configure API key input
    col_key1, col_key2 = st.columns([5, 5])
    with col_key1:
        st.markdown(
            "<p style='margin-bottom: 0px;'>If you already have your Albert API key, enter it here:</p>",
            unsafe_allow_html=True,
        )
    with col_key2:
        user_api_key = st.text_input(
            " ", type="password", key="user_api_key_launch", label_visibility="collapsed"
        )

    st.write(
        "If you do not have an Albert API key, please request one using the [contact form](https://albert.sites.beta.gouv.fr/access/). You will receive a reply within 24 working hours."  # noqa: E501
    )

    if user_api_key:
        st.subheader("Configure the AI system to test")
        col1, col2, col3 = st.columns(3)
        with col1:
            public_collections = get_public_collections(user_api_key if user_api_key else "")
            collection_names = [col["name"] for col in public_collections]
            collections_selected_names = st.multiselect(
                "Public Collections",
                options=collection_names,
                key="main_collection_select",
            )
            collections_selected_ids = [
                col["id"] for col in public_collections if col["name"] in collections_selected_names
            ]
        with col2:
            st.selectbox("LLM", DEFAULT_MODEL, key="selected_llm")
        with col3:
            selected_prompt = st.selectbox(
                "Select a prompt", ["Select prompt"] + PROMPT_CHOICES, key="selected_prompt"
            )

        st.subheader("Define evaluation parameters")
        col4, col5, col6 = st.columns(3)
        with col4:
            datasets = list_datasets()
            dataset = st.selectbox(
                "Select a test dataset", ["Select dataset"] + datasets, key="main_dataset_select"
            )
        with col5:
            st.selectbox("LLM Judge", DEFAULT_JUDGE_MODEL, key="selected_judge")
        with col6:
            selected_metrics = st.multiselect(
                "Select generation metrics", options=CHOICE_METRICS, key="selected_metrics"
            )

        if selected_metrics:
            selected_metrics_list = [m.strip() for m in selected_metrics if m.strip()]
        else:
            selected_metrics_list = []

        METRICS_FOR_EXPSET = selected_metrics_list + DEFAULT_METRICS

        st.divider()

        try:
            experimentset = create_experiment_set(
                dataset=dataset,
                collection_ids=collections_selected_ids,
                model_name=DEFAULT_MODEL,
                prompt=selected_prompt if selected_prompt and selected_prompt != "Select prompt" else "",
                judge_model=DEFAULT_JUDGE_MODEL,
                api_key=user_api_key,
                metrics=METRICS_FOR_EXPSET,
            )
        except Exception as e:
            st.error(f"Error creating experiment set: {e}")

        # Buttons and copy code with API key masked
        empty_col, button_col1, button_col2 = st.columns([8, 3, 3])
        with button_col1:
            run_button = st.button("Run Evaluation 🚀", key="eval_button")

        if run_button:
            if not user_api_key:
                st.error("Merci de renseigner votre clé d'accès avant de lancer une évaluation.")
            else:
                try:
                    result = post_experiment_set(experimentset, user_api_key)
                    if result and "id" in result:
                        expset_id = result["id"]
                        st.success(f"Experiment set created: {result['name']} (ID: {expset_id})")

                        dashboard_url = f"/experiments_set?expset={expset_id}"
                        st.markdown(button_style, unsafe_allow_html=True)
                        st.markdown(
                            f'<a href="{dashboard_url}" class="custom-button">See detailed results in the dashboard</a>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.error("Error creating experiment set")
                except Exception as e:
                    st.error(f"Error creating experiment set : {e}")

        with button_col2:
            with st.popover("📋 Copy code"):
                try:
                    # Clone experimentset and substitute api_key by placeholder
                    exp_for_code = copy.deepcopy(experimentset)
                    if "cv" in exp_for_code and "grid_params" in exp_for_code["cv"]:
                        for model_cfg in exp_for_code["cv"]["grid_params"].get("model", []):
                            if "api_key" in model_cfg:
                                model_cfg["api_key"] = "YOUR_MODEL_API_KEY"

                    if "cv" in exp_for_code and "common_params" in exp_for_code["cv"]:
                        if "judge_model" in exp_for_code["cv"]["common_params"]:
                            jm = exp_for_code["cv"]["common_params"]["judge_model"]
                            if isinstance(jm, dict) and "api_key" in jm:
                                jm["api_key"] = "YOUR_MODEL_API_KEY"

                    st.markdown(
                        "This code allows you to reproduce an experiment set.  \n"
                        "**Caution**: the code might be incomplete, review it carefully and uses it at your own risks"
                    )

                    col1, col2 = st.columns([0.7, 0.3])
                    with col1:
                        copy_format = st.radio("Format:", ["Python", "cURL"], key="copy_format")
                        if copy_format == "Python":
                            code = template_manager.render_python(**exp_for_code)
                            lang = "python"
                        else:
                            code = template_manager.render_curl(**exp_for_code)
                            lang = "bash"

                    with col2:
                        copy_to_clipboard_button(code, button_id="copy_btn")

                    st.code(code, language=lang)

                except Exception as e:
                    st.error(f"Failed: to render copy code template: {e}")


main()
