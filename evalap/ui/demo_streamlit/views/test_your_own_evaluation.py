import copy
import json
import os
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components
from template_manager import TemplateManager
from utils import fetch

# ============================================================================
# CONSTANTS
# ============================================================================

EVALAP_FRONTEND_TOKEN = os.getenv("EVALAP_FRONTEND_TOKEN")

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

DEFAULT_DATASETS = [
    "llm-values-CIVICS",
    "lmsys-toxic-chat",
    "DECCP",
    "test_service_public",
    "test_annuaire_entreprises",
]

REQUIRED_GOLD_COLUMNS = {"query", "output_true"}
REQUIRED_AI_SYSTEM_COLUMN = "answer"

# ============================================================================
# DATASET OPERATIONS
# ============================================================================


def _should_skip_dataset(dataset: Dict[str, Any]) -> bool:
    if "output" in dataset.get("columns", []):
        return True
    if dataset.get("name") in DEFAULT_DATASETS:
        return True
    return False


def list_datasets() -> List[str]:
    datasets = fetch("get", "/datasets")
    if not datasets:
        st.warning("No dataset available")
        return []

    filtered = [ds["name"] for ds in datasets if not _should_skip_dataset(ds)]

    if not filtered:
        st.warning("No datasets available among the filtered datasets.")
        return []

    return filtered


# ============================================================================
# API KEY VALIDATION
# ============================================================================


def validate_provider_api_key(provider_name: str, api_key: str, model_name: str) -> Tuple[bool, Optional[str]]:
    if not api_key or not api_key.strip():
        return False, "API key is empty"

    if provider_name not in PROVIDER_URLS:
        return False, f"Unknown provider: {provider_name}"

    base_url = PROVIDER_URLS[provider_name]

    try:
        if provider_name == "Anthropic":
            response = requests.get(
                "https://api.anthropic.com/v1/models",
                headers={"x-api-key": api_key, "anthropic-version": "2023-06-01"},
                timeout=10,
            )
        else:
            response = requests.get(
                f"{base_url}/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10,
            )

        if response.status_code == 200:
            return True, None
        elif response.status_code == 401:
            return False, "Invalid API key"
        elif response.status_code == 403:
            return False, "Access forbidden - check your API key permissions"
        else:
            return False, f"Authentication failed (status {response.status_code})"

    except requests.exceptions.Timeout:
        return False, "Request timeout - please try again"
    except requests.exceptions.RequestException as e:
        return False, f"Network error: {str(e)}"
    except Exception as e:
        return False, f"Validation error: {str(e)}"


# ============================================================================
# EXPERIMENT SET OPERATIONS
# ============================================================================


def create_experiment_set(
    dataset: str,
    model_alias: str,
    your_ia_system: Any,
    judge_url: str,
    judge_model: str,
    api_key_judge: str,
    metrics: List[str],
) -> Dict[str, Any]:
    if your_ia_system == "change for file upload":
        your_ia_system = st.session_state.get("your_ia_system")
        if your_ia_system is None:
            raise ValueError("No AI system file uploaded. Please upload a CSV file first.")

    if not isinstance(your_ia_system, pd.DataFrame):
        raise ValueError("Invalid AI system data format")

    if REQUIRED_AI_SYSTEM_COLUMN not in your_ia_system.columns:
        raise ValueError(f"The uploaded file must contain an '{REQUIRED_AI_SYSTEM_COLUMN}' column")

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
                "output": your_ia_system[REQUIRED_AI_SYSTEM_COLUMN].values.tolist(),
            },
        ]
    }

    expset_name = "NAME ***"  # TODO change
    expset_readme = "README ***"  # TODO change

    expset = {
        "name": expset_name,
        "readme": expset_readme,
        "cv": {"common_params": common_params, "grid_params": grid_params, "repeat": 1},
    }

    return expset


def post_experiment_set(expset: Dict[str, Any], token: str) -> Optional[Dict[str, Any]]:
    return fetch("post", "/experiment_set", data=expset, token=token)


def mask_api_keys_in_experimentset(experimentset: Dict[str, Any]) -> Dict[str, Any]:
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


# ============================================================================
# UI COMPONENTS
# ============================================================================


def info_banner(text: str) -> None:
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


def copy_to_clipboard_button(text_to_copy: str, button_id: str = "copy_btn", height: int = 60) -> None:
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


def render_copy_code_popover(experimentset: Dict[str, Any]) -> None:
    template_manager = TemplateManager()

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
                copy_format = st.radio("Format:", ["Python", "cURL"], key="copy_format_test_tab")

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


# ============================================================================
# GOLD DATASET UPLOAD
# ============================================================================


def _verify_user_api_key(user_api_key: str) -> bool:
    if not user_api_key:
        st.warning("⚠️ Please enter your EvalAP access key to upload a gold dataset.")
        return False

    with st.spinner("Verifying your access key..."):
        verif_authent = fetch("get", "/metrics", token=user_api_key, show_error=False)

    if verif_authent is None:
        st.error("❌ Your EvalAP access key is invalid.")
        st.info(
            "If you do not have an EvalAP access key, request one via the "
            "[Tchap channel](https://www.tchap.gouv.fr/#/room/!gpLYRJyIwdkcHBGYeC:agent.dinum.tchap.gouv.fr)"
        )
        return False

    st.success("✅ Access key validated")
    return True


def _handle_file_upload() -> Optional[Any]:
    uploaded_gold_file = st.file_uploader(
        "Upload your gold dataset (CSV or Excel)",
        type=["csv", "xls", "xlsx"],
        key="gold_dataset_uploader",
        help="File must contain at least 'query' and 'output_true' columns",
    )

    if uploaded_gold_file is not None:
        if (
            "uploaded_gold_file" not in st.session_state
            or st.session_state["uploaded_gold_file"].name != uploaded_gold_file.name
        ):
            st.session_state["uploaded_gold_file"] = uploaded_gold_file
            st.session_state["gold_dataset_loaded"] = False
            if "gold_dataset_name" not in st.session_state:
                st.session_state["gold_dataset_name"] = uploaded_gold_file.name.split(".")[0]
            if "gold_dataset_readme" not in st.session_state:
                st.session_state["gold_dataset_readme"] = ""
    else:
        if "uploaded_gold_file" in st.session_state:
            uploaded_gold_file = st.session_state["uploaded_gold_file"]
        else:
            st.info("📁 Please upload a gold dataset file")
            return None

    return uploaded_gold_file


def _load_and_validate_dataset(uploaded_file: Any) -> None:
    try:
        uploaded_file.seek(0)

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, delimiter=";", on_bad_lines="skip")
        else:
            df = pd.read_excel(uploaded_file)

        if REQUIRED_GOLD_COLUMNS.issubset(set(df.columns)):
            st.session_state["loaded_gold_df"] = df
            st.session_state["gold_dataset_loaded"] = True
            st.success(f"✅ File loaded successfully: {len(df)} rows detected")

            with st.expander("📋 Preview data", expanded=True):
                st.dataframe(df.head(10), use_container_width=True)
                st.caption(f"Columns: {', '.join(df.columns)}")
        else:
            st.session_state["gold_dataset_loaded"] = False
            st.error(
                f"❌ The file must contain at least 'query' and 'output_true' columns. "
                f"Found columns: {', '.join(df.columns)}"
            )
    except Exception as e:
        st.session_state["gold_dataset_loaded"] = False
        st.error(f"❌ Error loading file: {e}")


def _send_dataset_to_api(user_api_key: str) -> None:
    current_name = st.session_state.get("gold_dataset_name", "")
    current_readme = st.session_state.get("gold_dataset_readme", "")
    df_to_send = st.session_state.get("loaded_gold_df", None)

    if not current_name or not current_name.strip():
        st.error("❌ Please provide a dataset name")
        return

    if df_to_send is None:
        st.error("❌ No dataset loaded to send")
        return

    with st.spinner(f"Sending dataset '{current_name}' to API..."):
        dataset = {
            "name": current_name,
            "df": df_to_send.to_json(),
            "readme": current_readme,
            "default_metric": "judge_notator",
        }
        result = fetch("post", "/dataset", dataset, user_api_key)

    if result:
        st.success(f"✅ Dataset created successfully: **{current_name}** (ID: {result.get('id')})")

        # Clean up session state
        for key in ["uploaded_gold_file", "loaded_gold_df"]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state["gold_dataset_loaded"] = False

        st.info("💡 Refresh the page to see your new dataset in the dropdown list")
    else:
        st.error("❌ Error creating the dataset. Please check your data and try again.")


def handle_gold_dataset_upload() -> None:
    user_api_key = st.text_input(
        "Enter your EvalAP access key",
        type="password",
        key="gold_dataset_api_key",
        help="You need an EvalAP access key. Request one via the Tchap channel.",
    )

    if not _verify_user_api_key(user_api_key):
        return

    uploaded_gold_file = _handle_file_upload()
    if uploaded_gold_file is None:
        return

    # Dataset name and description inputs
    st.text_input(
        "Dataset name",
        key="gold_dataset_name",
        help="Give a meaningful name to your gold dataset",
    )

    st.text_area(
        "Description (readme)",
        key="gold_dataset_readme",
        help="Describe your dataset (purpose, source, content, etc.)",
    )

    # Load and verify button
    if st.button("📊 Load and verify dataset", key="load_gold_dataset_btn"):
        _load_and_validate_dataset(uploaded_gold_file)

    # Send to API button
    if st.session_state.get("gold_dataset_loaded", False):
        if st.button(
            "🚀 Send dataset to EvalAP API",
            key="send_gold_dataset_btn",
            type="primary",
        ):
            _send_dataset_to_api(user_api_key)


# ============================================================================
# EVALUATION WORKFLOW
# ============================================================================


def handle_run_evaluation(experimentset: Dict[str, Any], is_valid: bool) -> None:
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


# ============================================================================
# UI
# ============================================================================


def _render_ai_system_upload_section() -> None:
    st.markdown("### Upload your AI system answers")

    st.markdown(
        "<p style='color:#666; margin-bottom:20px;'>Run your test query with your AI system, "
        "then download the CSV file containing the query and responses "
        "(named 'query' and 'answer' respectively).</p>",
        unsafe_allow_html=True,
    )

    col_upload1, col_btn1 = st.columns([8, 2])

    with col_upload1:
        uploaded_file = st.file_uploader(
            "Upload CSV",
            type=["csv"],
            key="ai_system_answers_upload",
            label_visibility="collapsed",
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

    if upload_btn_1 and uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)

            if REQUIRED_AI_SYSTEM_COLUMN not in df.columns:
                st.error(f"❌ The CSV file must contain an '{REQUIRED_AI_SYSTEM_COLUMN}' column")
            else:
                st.session_state["your_ia_system"] = df
                st.session_state["uploaded_dataset_name"] = uploaded_file.name.replace(".csv", "")
                st.success(f"✅ File uploaded: {uploaded_file.name} ({len(df)} rows)")

                with st.expander("📊 Preview uploaded data"):
                    st.dataframe(df.head(2))

        except Exception as e:
            st.error(f"❌ Error reading CSV file: {e}")


def _render_gold_dataset_selection() -> str:
    col1, col2 = st.columns([3, 7])

    with col1:
        st.markdown(
            "<p style='margin-top:8px; margin-bottom:0;'>Your Gold dataset</p>",
            unsafe_allow_html=True,
        )

    with col2:
        datasets = list_datasets()
        gold_file = st.selectbox(
            " ",
            ["Select dataset"] + datasets,
            key="gold_dataset_select",
            help="Choose the reference dataset that will be used to evaluate the test RAG system.",
        )

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    with st.expander("Load your gold dataset", expanded=False):
        st.markdown(
            """
        Your **gold dataset** is your reference dataset containing:
        - `query`: the questions/prompts
        - `output_true`: the expected correct answers

        ℹ️ **Note**: You only need to upload your gold dataset once.
        It will then be available in the dropdown above for all your experiments.
        """
        )
        handle_gold_dataset_upload()

    return gold_file


def _render_judge_model_configuration() -> Tuple[str, str, str, str, bool, Optional[str]]:
    col_provider_info, col_provider, col_model_info, col_model, col_api, col_api_key, col_status = st.columns(
        [3, 4, 3, 4, 3, 7, 3]
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
            help="Select the Provider LLM that will assess and score the system's answers.",
        )

    judge_provider_url = PROVIDER_URLS.get(judge_provider_name, "")

    with col_model_info:
        st.markdown("<p style='margin-bottom: 0px;'>Judge Model</p>", unsafe_allow_html=True)

    with col_model:
        judge_model = st.text_input(
            "",
            key="model_judge_test",
            placeholder="Input field",
            help="Inform the Model LLM that will assess and score the system's answers.",
        )

    with col_api:
        st.markdown("<p style='margin-top:8px;'>Your API key</p>", unsafe_allow_html=True)

    with col_api_key:
        api_key_judge = st.text_input(
            " ",
            type="password",
            key="api_key_judge_test",
            placeholder="Entrez votre clé API",
            help="Inform the API key LLM",
        )

    # Validate API key if all required fields are provided
    is_valid = False
    error_msg = None

    with col_status:
        if api_key_judge and judge_provider_name != "select provider" and judge_model:
            is_valid, error_msg = validate_provider_api_key(judge_provider_name, api_key_judge, judge_model)

            if is_valid:
                st.markdown(
                    """
                    <div style="
                        background-color:#d4f6dd;
                        border:1px solid #7ac89b;
                        padding:4px 6px;
                        border-radius:4px;
                        display:inline-block;
                        margin-top:4px;
                    ">
                        <span style="font-size:12px;">✅ Valid API key</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div style="
                        background-color:#ffd6d6;
                        border:1px solid:#ff9b9b;
                        padding:4px 6px;
                        border-radius:4px;
                        display:inline-block;
                        margin-top:4px;
                    ">
                        <span style="font-size:12px;">❌ {error_msg or "Invalid API key"}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    return judge_provider_name, judge_provider_url, judge_model, api_key_judge, is_valid, error_msg


def _render_metrics_selection() -> List[str]:
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
    return metrics


# ============================================================================
# MAIN
# ============================================================================


def render_test_tab() -> None:
    """Main function for rendering the Test tab interface."""
    # Section 1: Upload AI system answers
    _render_ai_system_upload_section()

    st.divider()

    # Section 2: Configure evaluation settings
    st.markdown("### Configure the evaluation settings")

    gold_file = _render_gold_dataset_selection()

    judge_provider_name, judge_provider_url, judge_model, api_key_judge, is_api_key_valid, error_msg = (
        _render_judge_model_configuration()
    )

    metrics = _render_metrics_selection()

    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    st.divider()

    # Validate configuration and create experiment set
    experimentset = None

    if is_api_key_valid:
        try:
            model_alias = "Model alias *****"  # TODO change
            your_ia_system_file = "change for file upload"

            experimentset = create_experiment_set(
                dataset=gold_file,
                model_alias=model_alias,
                your_ia_system=your_ia_system_file,
                judge_url=judge_provider_url,
                judge_model=judge_model,
                api_key_judge=api_key_judge,
                metrics=metrics,
            )
        except Exception as e:
            st.error(f"Error creating experiment set: {e}")

    # Action buttons
    empty_col, button_col1, button_col2 = st.columns([8, 3, 3])

    with button_col1:
        run_button = st.button(
            "Run test evaluation",
            key="my_own_eval_button",
            disabled=not is_api_key_valid,
        )

    with button_col2:
        if experimentset:
            render_copy_code_popover(experimentset)

    if run_button and is_api_key_valid:
        handle_run_evaluation(experimentset, is_api_key_valid)
