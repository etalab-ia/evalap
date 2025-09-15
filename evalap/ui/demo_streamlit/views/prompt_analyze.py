import os
from datetime import datetime
import streamlit as st
import requests
from utils import fetch

EVALAP_API_KEY = os.getenv("EVALAP_API_KEY")
ALBERT_API_KEY = os.getenv("ALBERT_API_KEY")

# config
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
DEFAULT_METHOD_COLLECTION = "semantic"


def styled_markdown(text):
    st.markdown(
        f"<span style='color: #000091; font-size: 1.0em; font-weight: bold;'>{text}</span>",
        unsafe_allow_html=True,
    )


def get_public_collections(api_key):
    url = f"{DEFAULT_PROVIDER_URL}/collections"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {DEFAULT_API_KEY}",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return [
            {"id": collection["id"], "name": collection["name"]}
            for collection in data["data"]
            if collection.get("visibility") == "public"
        ]
    else:
        st.error(f"Erreur récupération collections publiques : {response.status_code}")
        return []


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


def experimental_section(
    mode: str,
    session_key_models: str,
    session_key_prompts: str,
):
    assert mode in ("create", "patch")

    expander_label = "la création" if mode == "create" else "l'ajout de prompts"
    with st.expander(f"À propos de {expander_label}"):
        if mode == "create":
            st.markdown(
                """
                Pour créer une expérimentation qui compare différents prompts sur votre cas d'usage, il vous faut plusieurs éléments :  
                - un nom de produit auquel associer les tests. 
                - le dataset de l'expérimentation (on ne peut en sélectionner qu'un)
                - les collections (les documents qui servent de base de connaissances pour le système)
                - le(s) modèle(s) 
                - le/les prompts à évaluer 
                """
            )
        else:
            st.markdown(
                """
                Il vous faut :  
                - l'identifiant Id de l'expérimentation à enrichir  
                - le dataset de l'expérimentation (le même nom que celui associé à l'experiment set existant)
                - les collections (les documents qui servent de base de connaissances pour le système)
                - le(s) modèle(s) à ajouter aux tests
                - le(s) prompt(s) à ajouter aux tests
                """
            )

    st.markdown("### Données d'expérimentation")
    styled_markdown("Informations générales")

    cols = st.columns(3)

    if mode == "create":
        with cols[0]:
            product_name = st.text_input(
                "Nom du produit", placeholder="ex: Assistant IA", key="main_product_name"
            )
    else:
        with cols[0]:
            expset_id = st.text_input("ID de l'experiment set à enrichir", key="patch_expset_id")

    with cols[1]:
        datasets = list_datasets()
        dataset = st.selectbox(
            "Dataset d'évaluation",
            ["Sélectionner un dataset"] + datasets,
            key="main_dataset_select" if mode == "create" else "patch_dataset_select",
        )

    # Public Collection name from ALbert API
    public_collections = get_public_collections(DEFAULT_API_KEY)
    collection_names = [col["name"] for col in public_collections]

    with cols[2]:
        collections_selected_names = st.multiselect(
            "Collections publiques",
            options=collection_names,
            key="main_collection_select" if mode == "create" else "patch_collection_select",
        )

    collections_selected_ids = [
        col["id"] for col in public_collections if col["name"] in collections_selected_names
    ]

    model_selection = model_config_section(session_key_models)
    prompts = prompt_section(
        session_key_prompts, "Prompt à tester" if mode == "create" else "Prompt à ajouter"
    )

    st.divider()
    button_label = (
        "Évaluer les prompts 🚀" if mode == "create" else "Ajouter ces prompts à l'experimentation 🚀"
    )
    button_clicked = st.button(button_label)

    if button_clicked:
        if mode == "create" and (not product_name or dataset == "Sélectionner un dataset"):
            st.error("Merci de renseigner le nom du produit et de sélectionner un dataset valide.")
            return
        if mode == "patch":
            if not expset_id or expset_id.strip() == "":
                st.error("Merci de renseigner l'ID de l'experiment set à enrichir.")
                return
            if not dataset or dataset == "Sélectionner un dataset":
                st.error("Merci de sélectionner un dataset valide.")
                return
        if not prompts or all(not p.strip() for p in prompts):
            st.error("Veuillez saisir au moins un prompt.")
            return
        if not any(selected for selected in model_selection.values()):
            st.error("Veuillez sélectionner au moins un modèle.")
            return

        expset_name = None
        if mode == "create":
            expset_name = f"analyse_prompt_{product_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        common_params = {
            "dataset": dataset,
            "metrics": DEFAULT_METRICS,
            "judge_model": DEFAULT_JUDGE_MODEL,
        }

        model_configs = []
        for model_name, selected in model_selection.items():
            if selected:
                for prompt in prompts:
                    prompt = prompt.strip()
                    if prompt:
                        model_config = {
                            "name": model_name,
                            "base_url": DEFAULT_PROVIDER_URL,
                            "api_key": DEFAULT_API_KEY,
                            "system_prompt": prompt,
                            "sampling_params": {"temperature": DEFAULT_TEMPERATURE},
                        }
                        if collections_selected_ids:
                            model_config["extra_params"] = {
                                "search": True,
                                "search_args": {
                                    "method": DEFAULT_METHOD_COLLECTION,
                                    "collections": collections_selected_ids,
                                    "k": 10,
                                },
                            }
                        model_configs.append(model_config)

        if not model_configs:
            st.error("Aucun modèle ou prompt valide.")
            return

        headers = {"Authorization": f"Bearer {EVALAP_API_KEY}"}

        if mode == "create":
            expset = {
                "name": expset_name,
                "readme": "Baseline prompt",
                "cv": {
                    "common_params": common_params,
                    "grid_params": {"model": model_configs},
                    "repeat": 1,
                },
            }
            result = post_experiment_set(expset, headers)
            if result and "id" in result:
                st.success(f"Experiment set créé: {result['name']} (ID: {result['id']})")
                dashboard_url = f"/experiments_set?expset={result['id']}"
                st.markdown(f"[🔗 Voir les résultats détaillés dans le dashboard]({dashboard_url})")
            else:
                st.error("Erreur lors de la création de l'experiment set")
        else:
            patch_data = {
                "cv": {
                    "common_params": common_params,
                    "grid_params": {"model": model_configs},
                    "repeat": 1,
                }
            }
            result = patch_experiment_set(expset_id, patch_data, headers)
            if result:
                st.success(
                    f"Ajout avec succès dans l'expérience ID {expset_id} de {len(model_configs)} nouveau(x) modèle(s)/prompt(s)"
                )
            else:
                st.error("Patch impossible.")


def main():
    st.title("Expérimentations de prompt")
    st.write(
        "Vous pouvez ici expérimenter des prompts sur votre cas d'usage, "
        "en utilisant les modèles albert-large et/ou albert-small proposés par **Albert API**."
    )
    st.divider()

    tab1, tab2 = st.tabs(
        ["Création d'une expérimentation", "Ajouter des prompts à une experimentation existante"]
    )

    with tab1:
        experimental_section(mode="create", session_key_models="model_configs", session_key_prompts="prompts")

    with tab2:
        experimental_section(
            mode="patch", session_key_models="model_configs_patch", session_key_prompts="prompts_to_patch"
        )


main()
