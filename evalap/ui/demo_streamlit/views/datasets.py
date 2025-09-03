import json
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
