import copy
import json
import os

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from template_manager import TemplateManager
from utils import fetch

EVALAP_FRONTEND_TOKEN = os.getenv("EVALAP_FRONTEND_TOKEN")

# Configuration
PROVIDER_URLS = {
    "Albert API": "https://albert.api.etalab.gouv.fr/v1",
    "OpenAI": "https://api.openai.com/v1",
    "Anthropic": "https://api.anthropic.com/v1",
    "Mistral": "https://api.mistral.ai/v1",
}

DEFAULT_METRICS = [
    "generation_time",
    "nb_tokens_prompt",
    "nb_tokens_completion",
    "energy_consumption",
    "gwp_consumption",
]
CHOICE_METRICS = ["judge_notator", "judge_exactness"]

template_manager = TemplateManager()


def info_banner(text):
    """Display info banner with custom styling"""
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
            <span style="font-size:20px; font-weight:normal;">
                {text}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def post_experiment_set(expset, EVALAP_FRONTEND_TOKEN):
    return fetch("post", "/experiment_set", data=expset, token=EVALAP_FRONTEND_TOKEN)


def create_experiment_set(
    dataset,
    model_alias,
    your_ia_system,
    judge_url,
    judge_model,
    api_key_judge,
    metrics,
):
    if your_ia_system == "change for file upload":
        your_ia_system = st.session_state.get("your_ia_system")

        if your_ia_system is None:
            raise ValueError("No AI system file uploaded. Please upload a CSV file first.")

    if not isinstance(your_ia_system, pd.DataFrame):
        raise ValueError("Invalid AI system data format")

    if "answer" not in your_ia_system.columns:
        raise ValueError("The uploaded file must contain an 'answer' column")

    common_params = {
        "dataset": dataset,
        "metrics": metrics,
        "judge_model": {
            "name": judge_model,
            "base_url": judge_url,
            "api_key": api_key_judge,
        },
    }

    grid_params = {
        "model": [
            {
                "aliased_name": model_alias,
                "output": your_ia_system["answer"].values.tolist(),
            },
        ]
    }
    expset_name = "NAME ***"
    expset_readme = "README ***"
    expset = {
        "name": expset_name,
        "readme": expset_readme,
        "cv": {"common_params": common_params, "grid_params": grid_params, "repeat": 1},
    }
    st.write(expset)
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


def mask_api_keys_in_experimentset(experimentset):
    exp_for_code = copy.deepcopy(experimentset)

    if "cv" in exp_for_code and "grid_params" in exp_for_code["cv"]:
        for model_cfg in exp_for_code["cv"]["grid_params"].get("model", []):
            if "api_key" in model_cfg:
                model_cfg["api_key"] = "YOUR_MODEL_API_KEY"

    if "cv" in exp_for_code and "common_params" in exp_for_code["cv"]:
        judge_model = exp_for_code["cv"]["common_params"].get("judge_model")
        if isinstance(judge_model, dict) and "api_key" in judge_model:
            judge_model["api_key"] = "YOUR_MODEL_API_KEY"

    return exp_for_code


def render_copy_code_popover(experimentset):
    with st.popover("📋 Copy code"):
        try:
            exp_for_code = mask_api_keys_in_experimentset(experimentset)

            st.markdown(
                "This code allows you to reproduce an experiment set.  \n"
                "**Caution**: the code might be incomplete, review it carefully "
                "and uses it at your own risks"
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
            st.error(f"Failed to render copy code template: {e}")


def handle_run_evaluation(experimentset, is_valid):
    if not is_valid:
        st.error("Please enter your access key before starting an assessment.")
        return

    try:
        result = post_experiment_set(experimentset, EVALAP_FRONTEND_TOKEN)

        if result and "id" in result:
            expset_id = result["id"]
            st.success(f"Experiment set created: {result['name']} (ID: {expset_id})")

            dashboard_url = f"/experiments_set?expset={expset_id}"
            st.markdown(
                f'<a href="{dashboard_url}" class="custom-button">See detailed results in the dashboard</a>',
                unsafe_allow_html=True,
            )
        else:
            st.error("Error creating experiment set")

    except Exception as e:
        st.error(f"Error creating experiment set: {e}")


def render_test_tab():
    """Main function for Test tab"""

    # Section 1: Upload AI system answers
    st.markdown("### Upload your AI system answers")

    st.markdown(
        "<p style='color:#666; margin-bottom:20px;'>Run your test query with your AI system, then download the CSV file containing the query and responses.</p>",
        unsafe_allow_html=True,
    )

    col_upload1, col_btn1 = st.columns([8, 2])

    with col_upload1:
        uploaded_file = st.file_uploader(
            "Upload CSV", type=["csv"], key="ai_system_answers_upload", label_visibility="collapsed"
        )

    with col_btn1:
        st.markdown(
            """
            <style>
            div[data-testid="stButton"] button[kind="primary"] {
                background-color: #000091 !important;
                color: white !important;
                border: none !important;
            }
            div[data-testid="stButton"] button[kind="primary"]:hover {
                background-color: #1212FF !important;
            }
            </style>
        """,
            unsafe_allow_html=True,
        )

        upload_btn_1 = st.button(
            "Upload",
            key="upload_btn_1",
            disabled=uploaded_file is None,
            use_container_width=True,
            type="primary",
        )

    # Store uploaded dataset name in session state
    if upload_btn_1 and uploaded_file:
        try:
            # Read csv
            df = pd.read_csv(uploaded_file)

            if "answer" not in df.columns:
                st.error("❌ The CSV file must contain an 'answer' column")
            else:
                st.session_state["your_ia_system"] = df
                st.session_state["uploaded_dataset_name"] = uploaded_file.name.replace(".csv", "")
                st.success(f"✅ File uploaded: {uploaded_file.name} ({len(df)} rows)")

                with st.expander("📊 Preview uploaded data"):
                    st.dataframe(df.head(2))  # TODO drop

        except Exception as e:
            st.error(f"❌ Error reading CSV file: {e}")

    st.divider()

    # Section 2: Configure evaluation settings
    st.markdown("### Configure the evaluation settings")

    col1, col2 = st.columns([3, 7])

    with col1:
        st.markdown(
            "<p style='margin-top:8px; margin-bottom:0;'>Your Gold dataset</p>", unsafe_allow_html=True
        )

    with col2:
        datasets = ["dataset 1", "dataset 2"]  # list_datasets()
        gold_file = st.selectbox(
            " ",
            ["Select dataset"] + datasets,
            key="gold_dataset_select",
            help="Choose the reference dataset that will be used to evaluate the test RAG system.",
        )

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # Judge model and API key
    col_provider_info, col_provider, col_model_info, col_model, col_api, col_api_key = st.columns(
        [3, 4, 3, 4, 3, 7]
    )

    with col_provider_info:
        st.markdown("<p style='margin-bottom: 0px;'>Judge Provider</p>", unsafe_allow_html=True)

    with col_provider:
        judge_provider_options = [
            "select provider",
            "Albert API",
            "OpenAI",
            "Anthropic",
            "Mistral",
        ]
        judge_provider_name = st.selectbox(
            " ",
            judge_provider_options,
            key="provider_judge_test",
            help="Select the Provider LLM that will assess and score the system’s answers.",
        )
    judge_provider_url = PROVIDER_URLS.get(judge_provider_name, "")

    with col_model_info:
        st.markdown("<p style='margin-bottom: 0px;'>Judge Model</p>", unsafe_allow_html=True)

    with col_model:
        judge_model = st.text_input(
            "",
            key="model_judge_test",
            placeholder="Input field",
            help="Inform the Model LLM that will assess and score the system’s answers.",
        )

    with col_api:
        st.markdown("<p style='margin-top:8px;'>Your API key</p>", unsafe_allow_html=True)

    with col_api_key:
        api_key_judge = st.text_input(
            " ",
            type="password",
            key="api_key_judge_test",
            placeholder="Entrez votre clé API",
            help="Inform the API key LLM",  # Tooltip apparaît au survol du label
        )

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # Metrics
    col_metrics_title, col_metrics_choice, col_empty = st.columns([3, 7, 7])

    with col_metrics_title:
        st.markdown("<p style='margin-top:8px;'>Metrics</p>", unsafe_allow_html=True)

    with col_metrics_choice:
        selected_metrics = st.multiselect(
            "Select metrics",
            options=CHOICE_METRICS,
            key="metrics_test",
            placeholder="select metrics",
            label_visibility="collapsed",
        )

    metrics = (selected_metrics if selected_metrics else []) + DEFAULT_METRICS

    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)

    st.divider()

    experimentset = None
    model_alias = "Model alias *****"
    your_ia_system_file = "change for file upload"

    # Verif
    if "your_ia_system" not in st.session_state:
        st.warning("⚠️ Please upload your AI system answers CSV file first")
    elif gold_file == "Select dataset":
        st.warning("⚠️ Please select a Gold dataset")
    elif judge_provider_name == "select provider ":
        st.warning("⚠️ Please select a judge provider")
    elif not judge_model:
        st.warning("⚠️ Please select a judge model ")
    elif not api_key_judge:
        st.warning("⚠️ Please provide an API key for the judge model")
    else:
        try:
            experimentset = create_experiment_set(
                dataset=gold_file,
                model_alias=model_alias,
                your_ia_system=your_ia_system_file,
                judge_provider=judge_provider_url,
                judge_model=judge_model,
                api_key_judge=api_key_judge,
                metrics=metrics,
            )
        except Exception as e:
            st.error(f"Error creating experiment set: {e}")

    empty_col, button_col1, button_col2 = st.columns([8, 3, 3])

    with button_col1:
        run_button = st.button(
            "Run test evaluation",
            key="my_own_eval_button",
        )

    with button_col2:
        if experimentset:
            render_copy_code_popover(experimentset)

    is_api_key_valid = True  # TODO real verif if judge model acces tokenn
    if run_button and is_api_key_valid:
        handle_run_evaluation(experimentset, is_api_key_valid)
