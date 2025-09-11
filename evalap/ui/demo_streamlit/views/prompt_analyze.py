import os
import pandas as pd
from datetime import datetime
import streamlit as st
from utils import fetch

EVALAP_API_KEY = os.getenv("EVALAP_API_KEY")
ALBERT_API_KEY = os.getenv("ALBERT_API_KEY")

# default params
DEFAULT_JUDGE_MODEL = "gpt-4o1"
DEFAULT_METRICS = [
    "judge_notator",
    "judge_precision",
    "generation_time",
    "nb_tokens_prompt",
    "nb_tokens_completion",
    "energy_consumption",
    "gwp_consumption",
]
DEFAULT_TEMPERATURE = 0.2
DEFAULT_PROVIDER_URL = "https://albert.api.etalab.gouv.fr/v1"
DEFAULT_API_KEY = ALBERT_API_KEY


def _should_skip_dataset(dataset: dict) -> bool:
    return "output" in dataset.get("columns", [])


def list_datasets() -> list[str]:
    datasets = fetch("get", "/datasets")
    if not datasets:
        st.warning("Aucun dataset disponible")
        return []
    return [ds["name"] for ds in datasets if not _should_skip_dataset(ds)]


def post_dataset(dataset, headers):
    return fetch("post", "/dataset", dataset, headers)


def post_experiment_set(expset, headers):
    return fetch("post", "/experiment_set", data=expset, headers=headers)


def patch_experiment_set(expset_id, patch_data, headers):
    return fetch("patch", f"/experiment_set/{expset_id}", data=patch_data, headers=headers)


def model_config_section(session_key: str):
    """Gestion des modèles : choix limité à albert-large et albert-small, suppression conditionnelle"""
    if session_key not in st.session_state:
        st.session_state[session_key] = [
            {
                "provider": "albert-api",
                "model_name": "",
                "temperature": DEFAULT_TEMPERATURE,
                "provider_url": DEFAULT_PROVIDER_URL,
                "api_key": DEFAULT_API_KEY,
            }
        ]
    model_configs = st.session_state[session_key]

    def add_model():
        model_configs.append(
            {
                "provider": "albert-api",
                "model_name": "",
                "temperature": DEFAULT_TEMPERATURE,
                "provider_url": DEFAULT_PROVIDER_URL,
                "api_key": DEFAULT_API_KEY,
            }
        )

    def delete_model(i):
        if 0 <= i < len(model_configs) and len(model_configs) > 1:
            model_configs.pop(i)

    for i, config in enumerate(model_configs):
        cols = st.columns(2)
        with cols[0]:
            model_configs[i]["model_name"] = st.selectbox(
                f"Modèle #{i + 1}",
                options=["", "albert-large", "albert-small"],
                index=["", "albert-large", "albert-small"].index(config.get("model_name", ""))
                if config.get("model_name", "") in ["", "albert-large", "albert-small"]
                else 0,
                key=f"model_name_{session_key}_{i}",
            )
        with cols[1]:
            if len(model_configs) >= 2:
                st.write("")
                st.write("")
                if st.button("❌", key=f"delete_model_{session_key}_{i}"):
                    delete_model(i)
                    st.rerun()

    st.button("➕ Ajouter un modèle", on_click=add_model, key=f"add_model_button_{session_key}")
    return model_configs


def prompt_section(session_key: str, prompt_label: str = "Prompt", height: int = 100):
    """Gestion des prompts dynamiques (ajout, suppression), renvoie la liste"""
    if session_key not in st.session_state:
        st.session_state[session_key] = [""]

    prompts = st.session_state[session_key]

    def add_prompt():
        prompts.append("")

    def delete_prompt(i):
        if 0 <= i < len(prompts):
            prompts.pop(i)

    # Affichage premier prompt
    if prompts:
        cols = st.columns([8, 1])
        with cols[0]:
            prompts[0] = st.text_area(
                f"{prompt_label} #1", value=prompts[0], key=f"{session_key}_0", height=height
            )
        with cols[1]:
            if len(prompts) > 1 and st.button("❌", key=f"delete_{session_key}_0"):
                delete_prompt(0)
                st.rerun()

    st.button(f"➕ Ajouter un {prompt_label.lower()}", on_click=add_prompt)

    for i in range(1, len(prompts)):
        cols = st.columns([8, 1])
        with cols[0]:
            prompts[i] = st.text_area(
                f"{prompt_label} #{i + 1}", value=prompts[i], key=f"{session_key}_{i}", height=height
            )
        with cols[1]:
            if st.button("❌", key=f"delete_{session_key}_{i}"):
                delete_prompt(i)
                st.rerun()

    return prompts


def creation_experimental_section():
    with st.expander("À propos de la création d'une expérimentation"):
        st.markdown("""
            Pour créer une expérimentation qui compare différents prompts sur votre cas d'usage, il vous faut plusieurs éléments :  
            - un nom de produit auquel associé les tests. 
            - le dataset de l'expérimentation (on ne peut en sélectionner qu'un)
            - les collections (si RAG)
            - le modèle 
            - le/les prompts à évaluer 
        """)

    st.markdown("### Données d'expérimentation")
    st.caption("Disponible uniquement pour albert-large (pour le moment)")

    col1, col2, col3 = st.columns(3)

    with col1:
        product_name = st.text_input("Nom du produit", placeholder="ex: Assistant IA", key="main_product_name")
    with col2:
        datasets = list_datasets()
        dataset = st.selectbox(
            "Dataset d'évaluation", ["Sélectionner un dataset"] + datasets, key="main_dataset_select"
        )
    with col3:
        collection = st.selectbox(
            "Collections publiques (En construction)",
            ["Sélectionner collection", "Collection Publique 1", "Collection Publique 2"],
            key="main_collection_select",
        )

    model_configs = model_config_section("model_configs")
    prompts = prompt_section("prompts", "Prompt")

    st.divider()
    if st.button("Évaluer les prompts 🚀"):
        expset_name = f"analyse_prompt_{product_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        common_params = {
            "dataset": dataset,
            "metrics": DEFAULT_METRICS,
            "judge_model": DEFAULT_JUDGE_MODEL,
        }

        model_configs_for_exp = [
            {
                "name": cfg["model_name"],
                "base_url": DEFAULT_PROVIDER_URL,
                "api_key": DEFAULT_API_KEY,
                "system_prompt": prompt.strip(),
                "sampling_params": {"temperature": DEFAULT_TEMPERATURE},
            }
            for cfg in model_configs
            for prompt in prompts
            if cfg["model_name"] and prompt.strip()
        ]

        expset = {
            "name": expset_name,
            "readme": "Baseline prompt",
            "cv": {
                "common_params": common_params,
                "grid_params": {"model": model_configs_for_exp},
                "repeat": 1,
            },
        }

        headers = {"Authorization": f"Bearer {EVALAP_API_KEY}"}
        result = post_experiment_set(expset, headers)

        if result and "id" in result:
            expset_id = result["id"]
            st.success(f"Experiment set créé: {result['name']} (ID: {expset_id})")
            dashboard_url = f"/experiments_set?expset={expset_id}"
            st.markdown(f"[🔗 Voir les résultats détaillés dans le dashboard]({dashboard_url})")
        else:
            st.error("Erreur lors de la création de l'experiment set")


def patch_experimental_section():
    with st.expander("À propos de l'ajout de prompts"):
        st.markdown("""
            Il vous faut :  
            - l'identifiant Id de l'expérimentation à enrichir  
            - le dataset de l'expérimentation (le même nom que celui associé à l'experiment set existant)
            - le modèle à ajouter aux tests
            - le prompt à ajouter aux tests
        """)
    st.subheader("Ajouter des prompts à un experiment set existant (PATCH)")

    col1, col2 = st.columns(2)
    with col1:
        expset_id = st.text_input("ID de l'experiment set à enrichir", key="patch_expset_id")
    with col2:
        patch_dataset = st.selectbox(
            "Dataset d'évaluation à utiliser (PATCH)",
            ["Sélectionner un dataset"] + list_datasets(),
            key="patch_dataset_select",
        )

    model_configs_patch = model_config_section("model_configs_patch")
    prompts_patch = prompt_section("prompts_to_patch", "Prompt à patcher", height=80)

    st.divider()

    if st.button("Patch l'experiment set 🚀") and expset_id and patch_dataset and prompts_patch:
        models_to_patch = [
            {
                "name": cfg["model_name"],
                "base_url": DEFAULT_PROVIDER_URL,
                "api_key": DEFAULT_API_KEY,
                "system_prompt": prompt.strip(),
                "sampling_params": {"temperature": DEFAULT_TEMPERATURE},
            }
            for cfg in model_configs_patch
            for prompt in prompts_patch
            if cfg["model_name"] and prompt.strip()
        ]

        metrics = ["judge_notator", "generation_time", "nb_tokens_prompt", "energy_consumption"]

        new_model = {"model": models_to_patch}

        common_params = {
            "dataset": patch_dataset,
            "metrics": metrics,
            "judge_model": DEFAULT_JUDGE_MODEL,
        }

        patch_data = {
            "cv": {
                "common_params": common_params,
                "grid_params": new_model,
                "repeat": 1,
            }
        }

        headers = {"Authorization": f"Bearer {EVALAP_API_KEY}"}
        result = patch_experiment_set(expset_id, patch_data, headers)

        if result:
            st.success(
                f"Ajout avec succès dans l'expérience ID {expset_id} de {len(models_to_patch)} nouveau(x) modèle(s)/prompt(s)"
            )
        else:
            st.error("Patch impossible.")


def main():
    st.sidebar.title("EvalAP")
    st.sidebar.write("Mon tableau de bord (En construction)")
    st.sidebar.button("➕ Nouveau produit (En construction)", disabled=True)
    st.sidebar.button("➕ Nouveau dataset (En construction)", disabled=True)

    st.title("Expérimentations de prompt")
    st.subheader("Tâches complexes")

    st.divider()

    tab1, tab2 = st.tabs(
        ["Création d'une expérimentation", "Ajouter des prompts à une experimentation existante"]
    )

    with tab1:
        creation_experimental_section()

    with tab2:
        patch_experimental_section()


main()
