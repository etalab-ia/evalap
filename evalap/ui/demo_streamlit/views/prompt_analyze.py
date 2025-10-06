import os
from datetime import datetime

import requests
import streamlit as st
from utils import fetch

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
        f"<span style='color: #668bf2; font-size: 1.0em; font-weight: bold;'>{text}</span>",
        unsafe_allow_html=True,
    )


button_style = """
<style>
.custom-button {
    background-color: transparent;       /* Pas de fond */
    color: #000091;                      /* Texte bleu DSFR */
    border: 2px solid #000091;           /* Contour bleu DSFR */
    padding: 12px 28px;
    font-size: 20px;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
    text-align: center;
    text-decoration: none;
    display: inline-block;
}
.custom-button:hover {
    background-color: #000091;           /* Fond bleu DSFR au survol */
    color: white;                        /* Texte blanc au survol */
    border-color: #000091;
}
</style>
"""


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


def post_dataset(dataset, token):
    return fetch("post", "/dataset", dataset, token)


def post_experiment_set(expset, token):
    return fetch("post", "/experiment_set", data=expset, token=token)


def patch_experiment_set(expset_id, patch_data, token):
    return fetch("patch", f"/experiment_set/{expset_id}", data=patch_data, token=token)


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


def experimental_section(
    mode: str,
    session_key_models: str,
    session_key_prompts: str,
    user_api_key: str,
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
            result = post_experiment_set(expset, user_api_key)
            if result and "id" in result:
                expset_id = result["id"]
                st.success(f"Experiment set créé: {result['name']} (ID: {expset_id})")
                st.info(
                    "🚨 Note importante : conservez cet ID dans vos notes personnelles. "
                    "L'application est en version bêta et ne possède pas d'authentification ni de persistance."
                )

                dashboard_url = f"/experiments_set?expset={expset_id}"
                st.markdown(button_style, unsafe_allow_html=True)
                st.markdown(
                    f'<a href="{dashboard_url}" class="custom-button">Voir les résultats détaillés dans le dashboard</a>',
                    unsafe_allow_html=True,
                )
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
            result = patch_experiment_set(expset_id, patch_data, user_api_key)
            if result:
                st.success(
                    f"Ajout avec succès dans l'expérience ID {expset_id} de {len(model_configs)} nouveau(x) modèle(s)/prompt(s)"
                )
                st.info(
                    "🚨 Note importante : L'application est en version bêta, il se peut que les prompts ajoutés n'apparaissent pas de suite dans le dashboard. Il faut alors attendre un peu et cliquer sur le bouton refresh"
                )
                dashboard_url_patch = f"/experiments_set?expset={expset_id}"
                st.markdown(button_style, unsafe_allow_html=True)
                st.markdown(
                    f'<a href="{dashboard_url_patch}" class="custom-button">Voir les résultats détaillés dans le dashboard</a>',
                    unsafe_allow_html=True,
                )

            else:
                st.error("Patch impossible.")


def main():
    st.title("Expérimentations de prompt [BETA]")
    st.write(
        "L'experimentations de **prompt** est en phase bêta, uniquement pour évaluer des agents IA basés sur les **modèles** et **collections** publiques disponibles sur **Albert API**."
    )
    st.write(
        "Cette évaluation nécessite une clé d'accès EvalAP. Demander votre clé d'accès via le [canal Tchap](https://www.tchap.gouv.fr/#/room/!gpLYRJyIwdkcHBGYeC:agent.dinum.tchap.gouv.fr)"
    )
    st.divider()

    # USER API KEY
    user_api_key = st.text_input("Entrer votre clef d'accès", type="password", key="user_api_key_input")

    # Resetting prompts
    if "last_api_key" not in st.session_state:
        st.session_state["last_api_key"] = ""

    if user_api_key != st.session_state["last_api_key"]:
        st.session_state["last_api_key"] = user_api_key
        st.session_state["prompts"] = [""]
        st.session_state["prompts_to_patch"] = [""]
        st.session_state["model_configs"] = {
            "albert-large": False,
            "albert-small": False,
        }
        st.session_state["model_configs_patch"] = {
            "albert-large": False,
            "albert-small": False,
        }
    if not user_api_key:
        st.warning("Merci de renseigner votre clef d'accès.")
        st.stop()

    verif_authent = fetch("get", "/metrics", token=user_api_key, show_error=False)
    if verif_authent is None:
        st.error("Votre clé d'accès EvalAP est invalide.")
        st.info(
            "Si vous n'avez pas de clé d'accès EvalAP, demandez une clé via le [canal Tchap](https://www.tchap.gouv.fr/#/room/!gpLYRJyIwdkcHBGYeC:agent.dinum.tchap.gouv.fr)"
        )
        st.stop()

    tab1, tab2 = st.tabs(
        ["Création d'une expérimentation", "Ajouter des prompts à une experimentation existante"]
    )

    with tab1:
        experimental_section(
            mode="create",
            session_key_models="model_configs",
            session_key_prompts="prompts",
            user_api_key=user_api_key,
        )

    with tab2:
        experimental_section(
            mode="patch",
            session_key_models="model_configs_patch",
            session_key_prompts="prompts_to_patch",
            user_api_key=user_api_key,
        )


main()
