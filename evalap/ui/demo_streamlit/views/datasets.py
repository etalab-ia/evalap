from datetime import datetime
import pandas as pd
import streamlit as st
from utils import fetch
import json
from streamlit import session_state

session_state.layout = "wide"


def _fetch_dataset_id(id: int) -> dict:
    return fetch("get", f"/dataset/{id}")


def _fetch_dataset(id: int) -> dict:
    return fetch("get", "/dataset", {"id": id, "with_df": True})


def main():
    st.title("Datasets")

    datasets = fetch("get", "/datasets")
    if not datasets:
        return st.warning("No datasets yet to display")

    # Main content
    main_content, right_menu = st.columns([8, 2])

    with main_content:
        with st.container():
            st.write("""Avalaible datasets
                     """)

        for dataset in datasets:
            if "output" in dataset["columns"]:
                # @DEBUG: dataset to be removed soon (linked old experiments with the "upstream" dataset)
                continue

            when = datetime.fromisoformat(dataset["created_at"]).strftime("%d %B %Y")
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
                if st.button(f"👀  Show/Hide Data Preview", key=f"toggle_{dataset['id']}"):
                    if f"show_df_{dataset['id']}" not in st.session_state:
                        st.session_state[f"show_df_{dataset['id']}"] = False
                    st.session_state[f"show_df_{dataset['id']}"] = not st.session_state[
                        f"show_df_{dataset['id']}"
                    ]

                if st.session_state.get(f"show_df_{dataset['id']}", False):
                    with st.spinner("Loading dataset preview..."):
                        data = _fetch_dataset(dataset["id"])
                        if data:
                            df_str = data.get("df", "")
                            if df_str != "{}" and df_str.strip() != "":
                                try:
                                    df_json = json.loads(df_str)
                                    df = pd.DataFrame(df_json)
                                    if not df.empty:
                                        col_display1, col_display2 = st.columns(2)

                                        with col_display1:
                                            row_options = [
                                                10,
                                                50,
                                                100,
                                            ]
                                            available_options = [opt for opt in row_options if opt <= len(df)]

                                            max_available_option = (
                                                max(available_options) if available_options else 0
                                            )
                                            if len(df) > max_available_option or (
                                                len(df) not in available_options and len(df) <= 500
                                            ):
                                                available_options.append(f"All ({len(df)})")

                                            choice = st.radio(
                                                "Rows to display:",
                                                options=available_options,
                                                horizontal=True,
                                                key=f"rows_{dataset['id']}",
                                            )

                                            # Gérer le cas "All (X)"
                                            if isinstance(choice, str) and choice.startswith("All"):
                                                max_rows = len(df)
                                            else:
                                                max_rows = choice

                                        with col_display2:
                                            show_info = st.checkbox(
                                                "Show dataset info", key=f"info_{dataset['id']}"
                                            )

                                        st.dataframe(
                                            df.head(max_rows),
                                            use_container_width=True,
                                            height=min(400, max_rows * 35 + 100),
                                        )

                                        if show_info:
                                            with st.container(border=True):
                                                col_info1, col_info2 = st.columns(2)
                                                with col_info1:
                                                    st.success(
                                                        f"Dataset loaded: {len(df)} rows × {len(df.columns)} columns"
                                                    )

                                                with col_info2:
                                                    st.write("**Data types:**")
                                                    st.write(df.dtypes.to_frame("Type"))
                                    else:
                                        st.error("Failed to load dataset or dataset is empty")
                                except Exception as e:
                                    st.error(f"Error loading dataset: {str(e)}")
                            else:
                                st.info("No data available for preview")
                        else:
                            st.error("Failed to fetch dataset")

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
