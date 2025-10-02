import io
import json
import os
from datetime import datetime
from typing import Optional

import pandas as pd
import streamlit as st
from streamlit import session_state

from utils import fetch

session_state.layout = "wide"


def _fetch_dataset(id: int) -> dict:
    return fetch("get", "/dataset", {"id": id, "with_df": True})


def _toggle_preview_button(dataset_id: int, label: str = "👀 Show/Hide Data Preview") -> bool:
    if st.button(label, key=f"toggle_{dataset_id}"):
        state_key = f"show_df_{dataset_id}"
        st.session_state[state_key] = not st.session_state.get(state_key, False)
    return st.session_state.get(f"show_df_{dataset_id}", False)


def _parse_dataset_to_df(df_str: str) -> Optional[pd.DataFrame]:
    """Convert dataset JSON string into a DataFrame, or return None if invalid."""
    if not df_str or df_str.strip() in ("{}", ""):
        return None

    try:
        df_json = json.loads(df_str)
        df = pd.DataFrame(df_json)
        return df if not df.empty else None
    except (json.JSONDecodeError, ValueError, TypeError):
        return None


def _validate_uploaded_dataset(df: pd.DataFrame) -> bool:
    required_cols = {"query", "output_true"}
    df_cols = set(df.columns)
    return required_cols.issubset(df_cols)


def _post_dataset_to_api(name: str, df: pd.DataFrame, readme: str, user_api_key: str) -> dict:
    dataset = {
        "name": name,
        "df": df.to_json(),
        "readme": readme,
        "default_metric": "judge_notator",
    }

    response = fetch(
        "post",
        "/dataset",
        dataset,
        user_api_key,
    )
    return response


def _handle_file_upload(user_api_key: str):
    uploaded_file = st.file_uploader(
        "Upload dataset (CSV ou Excel)",
        type=["csv", "xls", "xlsx"],
        key="dataset_uploader",
        help="CSV or Excel file containing at least the columns 'query' and 'output_true'",
    )

    if uploaded_file is not None:
        # Do not reset dataset_loaded if same file uploaded
        if (
            "uploaded_file" not in st.session_state
            or st.session_state["uploaded_file"].name != uploaded_file.name
        ):
            st.session_state["uploaded_file"] = uploaded_file
            st.session_state["dataset_loaded"] = False  # reset if new file
            if "dataset_name" not in st.session_state:
                st.session_state["dataset_name"] = uploaded_file.name.split(".")[0]
            if "dataset_readme" not in st.session_state:
                st.session_state["dataset_readme"] = ""
    else:
        if "uploaded_file" in st.session_state:
            uploaded_file = st.session_state["uploaded_file"]
        else:
            uploaded_file = None

    if not uploaded_file:
        st.info("Please upload a dataset file to set name and description.")
        return

    st.text_input("Name of dataset", key="dataset_name")
    st.text_area("Description (readme)", key="dataset_readme")

    if st.button("Load and verify the dataset"):
        try:
            uploaded_file.seek(0)
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file, delimiter=";", on_bad_lines="skip")
            else:
                df = pd.read_excel(uploaded_file)

            if _validate_uploaded_dataset(df):
                st.session_state["loaded_df"] = df
                st.session_state["dataset_loaded"] = True
                st.success(f"File loaded successfully, {len(df)} rows detected.")
            else:
                st.session_state["dataset_loaded"] = False
                st.error("The file must contain at least the columns 'query' and 'output_true'.")
        except Exception as e:
            st.session_state["dataset_loaded"] = False
            st.error(f"Error loading file: {e}")

    if st.session_state.get("dataset_loaded", False):
        if st.button("Send the dataset to the EvalAP API"):
            current_name = st.session_state.get("dataset_name", "")
            current_readme = st.session_state.get("dataset_readme", "")
            df_to_send = st.session_state.get("loaded_df", None)

            if df_to_send is not None:
                result = _post_dataset_to_api(current_name, df_to_send, current_readme, user_api_key)
                if result:
                    st.success(f"Dataset created successfully: ID {result.get('id')}")
                    del st.session_state["uploaded_file"]
                    st.session_state["dataset_loaded"] = False
                    del st.session_state["loaded_df"]

                else:
                    st.error("Error creating the dataset.")
            else:
                st.error("No dataset loaded to send.")


def _load_dataset_preview(dataset_id: int) -> Optional[pd.DataFrame]:
    """Load a dataset preview with Streamlit feedback messages."""
    with st.spinner("Loading dataset preview..."):
        data = _fetch_dataset(dataset_id)
        if data is None:
            st.error("Failed to fetch dataset")
            return None

        df = _parse_dataset_to_df(data.get("df", ""))
        if df is None:
            st.info("No valid data available for preview")
            return None

        return df


def _render_dataset_dataframe(df: pd.DataFrame, dataset_id: int):
    col_display1, col_display2 = st.columns(2)
    with col_display1:
        row_options = [10, 50, 100]
        available_options = [opt for opt in row_options if opt <= len(df)]
        if len(df) > max(available_options, default=0) or (
            len(df) not in available_options and len(df) <= 500
        ):
            available_options.append(f"All ({len(df)})")

        choice = st.radio(
            "Rows to display:",
            options=available_options,
            horizontal=True,
            key=f"rows_{dataset_id}",
        )
        max_rows = len(df) if isinstance(choice, str) and choice.startswith("All") else choice

    with col_display2:
        show_info = st.checkbox("Show dataset info", key=f"info_{dataset_id}")

    st.dataframe(
        df.head(max_rows),
        use_container_width=True,
        height=min(400, max_rows * 35 + 100),
    )

    if show_info:
        with st.container(border=True):
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.success(f"Dataset loaded: {len(df)} rows × {len(df.columns)} columns")
            with col_info2:
                st.write("**Data types:**")
                st.write(df.dtypes.to_frame("Type"))


def _should_skip_dataset(dataset: dict) -> bool:
    """Check if dataset should be skipped from display."""
    return "output" in dataset.get("columns", [])


def _get_dataset_columns(dataset: dict) -> list:
    """Get dataset columns, preferring 'columns' over 'parquet_columns'."""
    return dataset["columns"] or dataset["parquet_columns"]


def add_dataset_section():
    st.info(
        """Your dataset must be loaded into EvalAP only once. It will then be accessible for all your experiments.
        You must give it a name and write a brief description that will be visible to everyone.
        The file must contain at least the question (called query) and the ground truth (called output_true). 
        You need to have an **EvalAP access key**, you can make the request in the [canal Tchap](https://www.tchap.gouv.fr/#/room/!gpLYRJyIwdkcHBGYeC:agent.dinum.tchap.gouv.fr) 
        """
    )

    user_api_key = st.text_input(
        "Enter your EvalAP access key", type="password", key="add_dataset_user_api_key"
    )

    if not user_api_key:
        st.warning("Please enter your EvalAP access key before adding a dataset.")
        return

    # Authentication verification
    verif_authent = fetch("get", "/metrics", token=user_api_key, show_error=False)
    if verif_authent is None:
        st.error("Your EvalAP access key is invalid.")
        st.info(
            "If you do not have an EvalAP access key, request one via the [canal Tchap](https://www.tchap.gouv.fr/#/room/!gpLYRJyIwdkcHBGYeC:agent.dinum.tchap.gouv.fr)"
        )
        return

    # If authenticated, show upload form
    _handle_file_upload(user_api_key)


def main():
    st.title("Datasets")

    datasets = fetch("get", "/datasets")
    if not datasets:
        return st.warning("No datasets yet to display")

    filtered_datasets = [dataset for dataset in datasets if not _should_skip_dataset(dataset)]

    # Main content layout
    main_content, right_menu = st.columns([8, 2])

    with main_content:
        st.write("Available datasets")

        with st.expander("Add new dataset", expanded=False):
            add_dataset_section()

        for dataset in filtered_datasets:
            when = datetime.fromisoformat(dataset["created_at"]).strftime("%d %B %Y")
            columns = _get_dataset_columns(dataset)

            with st.container():
                st.markdown(
                    f"<div id='{dataset['name'].lower().replace(' ', '-')}'></div>",
                    unsafe_allow_html=True,
                )
                st.subheader(dataset["name"])
                st.write(
                    f"Columns: {', '.join(map(lambda x: '**' + x + '**', dataset['columns'] or dataset['parquet_columns']))}"
                )
                if dataset["columns_map"]:
                    st.write(f"Columns map: {dataset['columns_map']}")

                st.markdown(dataset.get("readme", "No description available"))
                col1, col2, col3, col4 = st.columns([1 / 8, 2 / 8, 2 / 8, 3 / 8])
                with col1:
                    st.caption(f"Id: {dataset['id']} ")
                with col2:
                    st.caption(f"Rows: {dataset['size'] or dataset['parquet_size']}")
                with col3:
                    st.caption(f"Default metric: {dataset['default_metric']}")
                with col4:
                    st.caption(f"Created the {when}")

                # Dataset preview toggle and render
                if _toggle_preview_button(dataset["id"]):
                    df = _load_dataset_preview(dataset["id"])
                    if df is not None:
                        _render_dataset_dataframe(df, dataset["id"])

                st.divider()

    with right_menu:
        st.markdown("###### Quick Navigation")
        for dataset in datasets:
            if "output" in dataset["columns"]:
                # @DEBUG: dataset to be removed soon (linked old experiments with the "upstream" dataset)
                continue

            dataset_id = dataset["name"].lower().replace(" ", "-")
            st.markdown(
                f"""
                <a href="#{dataset_id}" style="color:grey;"
                   onclick="document.getElementById('{dataset_id}').scrollIntoView({{behavior: 'smooth'}});">
                    {dataset["name"]}
                </a><br>
            """,
                unsafe_allow_html=True,
            )


main()
