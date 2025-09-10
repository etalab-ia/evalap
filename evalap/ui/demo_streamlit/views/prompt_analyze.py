import os
import pandas as pd
from datetime import datetime
import streamlit as st
from utils import fetch

API_BASE_URL = os.getenv("API_BASE_URL")
EVALAP_API_KEY = os.getenv("EVALAP_API_KEY")
JUDGE = os.getenv("JUDGE", "gpt-4o-mini")


def _should_skip_dataset(dataset: dict) -> bool:
    return "output" in dataset.get("columns", [])


def list_datasets_section():
    datasets = fetch("get", "/datasets")
    if not datasets:
        st.warning("Aucun dataset disponible")
        return []
    return [ds["name"] for ds in datasets if not _should_skip_dataset(ds)]


def post_dataset(dataset, headers):
    return fetch("post", "/dataset", dataset, headers)


def post_experiment_set(expset, headers):
    return fetch("post", "/experiment_set", data=expset, headers=headers)


def main():
    st.sidebar.title("EvalAP")
    st.sidebar.write("Mon tableau de bord - non disponible pour le moment")
    st.sidebar.button("➕ Nouveau produit (En construction)", disabled=True)
    st.sidebar.button("➕ Nouveau dataset (En construction)", disabled=True)

    # En-tête principal et barre de déconnexion (en construction)
    cols = st.columns([6, 1])
    with cols[0]:
        st.title("Expérimentations de prompt")
        st.subheader("Tâches complexes")
    with cols[1]:
        st.markdown(
            "<div style='text-align:right'><a href='#'>Se déconnecter (En construction)</a></div>",
            unsafe_allow_html=True,
        )
    st.divider()

    # Section données d'expérimentation et saisie clef API

    st.markdown("### Données d'expérimentation")
    st.caption("Disponible uniquement pour Albert large (pour le moment)")

    # Section saisie produit, modèle, dataset, collection
    col1, col2, col3 = st.columns(3)
    with col1:
        product_name = st.text_input("Nom du produit", placeholder="ex: Assistant IA")
    with col2:
        datasets = list_datasets_section()
        dataset = st.selectbox("Dataset d'évaluation", ["Sélectionner dataset"] + datasets)
    with col3:
        collection = st.selectbox(
            "Collections publiques (En construction)",
            ["Sélectionner collection", "Collection Publique 1", "Collection Publique 2"],
        )

    col_model1, col_model2, col_model3, col_model4 = st.columns(4)

    with col_model1:
        modele = st.selectbox("Modèle utilisé", ["Sélectionner modèle", "albert-large"])
    with col_model2:
        PROVIDER = st.selectbox(
            "Provider",
            [
                "albert-api",
            ],
        )
    with col_model3:
        PROVIDER_URL = st.text_input("URL du provider", "https://albert.api.etalab.gouv.fr/v1")
    with col_model4:
        PROVIDER_API_KEY = st.text_input("Clef API", type="password", placeholder="sk-...")

    st.write(PROVIDER_API_KEY)

    # Gestion dynamique des prompts à tester dans st.session_state
    if "prompts" not in st.session_state:
        st.session_state.prompts = [""]

    def add_prompt():
        st.session_state.prompts.append("")

    def delete_prompt(index):
        if 0 <= index < len(st.session_state.prompts):
            st.session_state.prompts.pop(index)

    st.divider()

    st.subheader("Prompts à tester")
    st.button("➕ Ajouter un prompt", on_click=add_prompt)

    for i, prompt in enumerate(st.session_state.prompts):
        cols = st.columns([8, 1])
        with cols[0]:
            st.session_state.prompts[i] = st.text_area(
                f"Prompt #{i + 1}", value=prompt, key=f"prompt_{i}", height=100
            )
        with cols[1]:
            if st.button("❌", key=f"delete_{i}"):
                delete_prompt(i)
                st.experimental_rerun()

    # Bouton d'évaluation des prompts
    if st.button("Évaluer les prompts 🚀"):
        expset_name = f"analyse_prompt_{product_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        metrics = [
            "judge_notator",
            "judge_precision",
            "generation_time",
            "nb_tokens_prompt",
            "nb_tokens_completion",
            "energy_consumption",
            "gwp_consumption",
        ]
        common_params = {
            "dataset": dataset,
            "model": {"sampling_params": {"temperature": 0.2}},
            "metrics": metrics,
            "judge_model": JUDGE,
        }

        model_configs = [
            {
                "name": modele,
                "base_url": PROVIDER_URL,
                "api_key": PROVIDER_API_KEY,
                "system_prompt": prompt.strip(),
            }
            for prompt in st.session_state.prompts
            if prompt.strip()
        ]

        expset = {
            "name": expset_name,
            "readme": "Baseline prompt",
            "cv": {
                "common_params": common_params,
                "grid_params": {"model": model_configs},
                "repeat": 1,
            },
        }

        headers = {"Authorization": f"Bearer {os.getenv('EVALAP_API_KEY')}"}
        result = post_experiment_set(expset, headers)

        if result and "id" in result:
            expset_id = result["id"]
            st.success(f"Experiment set créé: {result['name']} (ID: {expset_id})")
            dashboard_url = f"{API_BASE_URL}/experiments_set?expset={expset_id}"
            st.markdown(f"[🔗 Voir les résultats détaillés dans le dashboard]({dashboard_url})")
        else:
            st.error("Erreur lors de la création de l'experiment set")


main()
