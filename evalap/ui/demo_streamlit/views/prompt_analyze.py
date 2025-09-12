import os
from datetime import datetime
import streamlit as st
from utils import fetch

EVALAP_API_KEY = os.getenv("EVALAP_API_KEY")
ALBERT_API_KEY = os.getenv("ALBERT_API_KEY")

DEFAULT_JUDGE_MODEL = "gpt-4.1"
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


def styled_markdown(text):
    st.markdown(
        f"<span style='color: #000091; font-size: 1.0em; font-weight: bold;'>{text}</span>",
        unsafe_allow_html=True,
    )


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
    if session_key not in st.session_state or not isinstance(st.session_state[session_key], dict):
        st.session_state[session_key] = {
            "albert-large": False,
            "albert-small": False,
        }
    model_selection = st.session_state[session_key]

    styled_markdown("Modèles Albert API")
    cols = st.columns(8)
    with cols[0]:
        model_selection["albert-large"] = st.checkbox(
            "albert-large",
            value=model_selection["albert-large"],
            key=f"{session_key}_albert_large",
        )
    with cols[1]:
        model_selection["albert-small"] = st.checkbox(
            "albert-small",
            value=model_selection["albert-small"],
            key=f"{session_key}_albert_small",
        )

    return model_selection


def prompt_section(session_key: str, prompt_label: str = "Prompt", height: int = 100):
    styled_markdown("Prompts à tester")

    if session_key not in st.session_state:
        st.session_state[session_key] = [""]

    prompts = st.session_state[session_key]

    def add_prompt():
        prompts.append("")

    def delete_prompt(i):
        if 0 <= i < len(prompts):
            prompts.pop(i)

    if prompts:
        cols = st.columns([8, 1])
        with cols[0]:
            prompts[0] = st.text_area(
                f"{prompt_label} #1", value=prompts[0], key=f"{session_key}_0", height=height
            )
        with cols[1]:
            if len(prompts) > 1 and st.button("❌", key=f"delete_{session_key}_0"):
                delete_prompt(0)
                st.experimental_rerun()

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
                st.experimental_rerun()

    return prompts


def creation_experimental_section():
    with st.expander("À propos de la création d'une expérimentation"):
        st.markdown(
            """
            Pour créer une expérimentation qui compare différents prompts sur votre cas d'usage, il vous faut plusieurs éléments :  
            - un nom de produit auquel associé les tests. 
            - le dataset de l'expérimentation (on ne peut en sélectionner qu'un)
            - les collections (si RAG)
            - le(s) modèle(s) 
            - le/les prompts à évaluer 
        """
        )

    st.markdown("### Données d'expérimentation")
    styled_markdown("Informations générales")

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

    model_selection = model_config_section("model_configs")
    prompts = prompt_section("prompts", "Prompt")

    st.divider()
    if st.button("Évaluer les prompts 🚀"):
        if not product_name or dataset == "Sélectionner un dataset":
            st.error("Merci de renseigner le nom du produit et de sélectionner un dataset valide.")
            return
        expset_name = f"analyse_prompt_{product_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        common_params = {
            "dataset": dataset,
            "metrics": DEFAULT_METRICS,
            "judge_model": DEFAULT_JUDGE_MODEL,
        }

        model_configs_for_exp = []
        for model_name, selected in model_selection.items():
            if selected:
                for prompt in prompts:
                    if prompt.strip():
                        model_configs_for_exp.append(
                            {
                                "name": model_name,
                                "base_url": DEFAULT_PROVIDER_URL,
                                "api_key": DEFAULT_API_KEY,
                                "system_prompt": prompt.strip(),
                                "sampling_params": {"temperature": DEFAULT_TEMPERATURE},
                            }
                        )

        if not model_configs_for_exp:
            st.error("Veuillez sélectionner au moins un modèle et saisir au moins un prompt.")
            return

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
        st.markdown(
            """
            Il vous faut :  
            - l'identifiant Id de l'expérimentation à enrichir  
            - le dataset de l'expérimentation (le même nom que celui associé à l'experiment set existant)
            - le(s) modèle(s) à ajouter aux tests
            - le prompt à ajouter aux tests
        """
        )
    st.subheader("Ajouter des prompts à une experimentation existante")
    styled_markdown("Informations sur l'expérimentation")

    col1, col2 = st.columns(2)
    with col1:
        expset_id = st.text_input("ID de l'experiment set à enrichir", key="patch_expset_id")
    with col2:
        patch_dataset = st.selectbox(
            "Dataset d'évaluation à utiliser",
            ["Sélectionner un dataset"] + list_datasets(),
            key="patch_dataset_select",
        )

    model_selection_patch = model_config_section("model_configs_patch")
    prompts_patch = prompt_section("prompts_to_patch", "Prompt à ajouter", height=80)

    st.divider()

    if (
        st.button("Ajouter ces prompts à l'experimentation 🚀")
        and expset_id
        and patch_dataset
        and prompts_patch
    ):
        models_to_patch = []
        for model_name, selected in model_selection_patch.items():
            if selected:
                for prompt in prompts_patch:
                    if prompt.strip():
                        models_to_patch.append(
                            {
                                "name": model_name,
                                "base_url": DEFAULT_PROVIDER_URL,
                                "api_key": DEFAULT_API_KEY,
                                "system_prompt": prompt.strip(),
                                "sampling_params": {"temperature": DEFAULT_TEMPERATURE},
                            }
                        )

        if not models_to_patch:
            st.error("Veuillez sélectionner au moins un modèle et saisir au moins un prompt pour patcher.")
            return

        new_model = {"model": models_to_patch}

        common_params = {
            "dataset": patch_dataset,
            "metrics": DEFAULT_METRICS,
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
    st.title("Expérimentations de prompt")
    st.write(
        "Vous pouvez ici experimenter des prompts sur votre cas d'usage, en utilisant les modèles albert-large et/ou albert_small proposés par **Albert API**. "
    )
    st.divider()

    tab1, tab2 = st.tabs(
        ["Création d'une expérimentation", "Ajouter des prompts à une experimentation existante"]
    )

    with tab1:
        creation_experimental_section()

    with tab2:
        patch_experimental_section()


main()
