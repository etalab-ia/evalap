import io
import json
import os
from datetime import datetime
from typing import Optional

import pandas as pd
import streamlit as st
from streamlit import session_state

from utils import fetch

EVALAP_API_KEY = os.getenv("EVALAP_API_KEY")

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


def _post_dataset_to_api(name: str, df: pd.DataFrame, readme: str = "") -> dict:
    dataset = {
        "name": name,
        "df": df.to_json(),
        "readme": readme,
        "default_metric": "judge_notator",
    }

    headers = {"Authorization": f"Bearer {EVALAP_API_KEY}"}
    response = fetch("post", "/dataset", dataset, headers)
    return response


def _handle_file_upload():
    uploaded_file = st.file_uploader(
        "Upload dataset (CSV ou Excel)",
        type=["csv", "xls", "xlsx"],
        key="dataset_uploader",
        help="CSV or Excel file containing at least the columns ‘query’ and 'output_true'",
    )

    if uploaded_file is not None:
        st.session_state["uploaded_file"] = uploaded_file
    elif "uploaded_file" in st.session_state:
        uploaded_file = st.session_state["uploaded_file"]

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                try:
                    df = pd.read_csv(uploaded_file, delimiter=";", on_bad_lines="skip")
                except Exception:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, on_bad_lines="skip")
            else:
                df = pd.read_excel(uploaded_file)

            # Check columns
            if _validate_uploaded_dataset(df):
                st.success(f"File load with success, {len(df)} detected lines.")

                # User input info
                name = st.text_input(
                    "Name of dataset", value=uploaded_file.name.split(".")[0], key="dataset_name"
                )
                readme = st.text_area("Description (readme)", key="dataset_readme")

                if st.button("Send the dataset to the EvalAP API"):
                    result = _post_dataset_to_api(name, df, readme)
                    if result:
                        st.success(f"Dataset created successfully : ID {result.get('id')}")
                        del st.session_state["uploaded_file"]
                    else:
                        st.error("Error creating dataset")

            else:
                st.error("Le fichier doit contenir au moins les colonnes 'query' et 'output_true'.")
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier : {e}")


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


def main():
    st.title("Datasets")

    datasets = fetch("get", "/datasets")
    if not datasets:
        return st.warning("No datasets yet to display")

    filtered_datasets = [dataset for dataset in datasets if not _should_skip_dataset(dataset)]

    # Main content
    main_content, right_menu = st.columns([8, 2])

    with main_content:
        with st.container():
            st.write("""Avalaible datasets
                     """)

        with st.expander("Add new dataset", expanded=False):
            st.info(
                """Your dataset must be loaded into EvalAP only once. It will then be accessible for all your experiments.
                You must give it a name and write a brief description that will be visible to everyone.
                The file must contain at least the question (called query) and the ground truth (called output_true)."""
            )
            _handle_file_upload()

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

                # See dataset content if df
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
