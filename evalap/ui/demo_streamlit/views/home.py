import os
from pathlib import Path

import streamlit as st
from PIL import Image
from routes import ROUTES

# from streamlit_card import card


def get_logo(filename="evalap_logo.png"):
    img_path = Path(__file__).resolve().parents[1] / "static" / "images"
    logo_path = img_path / filename
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
    else:
        logo = Image.New("RGBA", (200, 100), (255, 255, 255, 0))
    return logo


col1, col2, _ = st.columns([0.2, 0.6, 0.2])  # Image column is 20%, content column is 60%

with col1:
    st.image(get_logo(), width=150)

with col2:
    st.title("Bienvenue sur EvalAP")


st.markdown(
    """
    <style>
    /* DSFR Blue and styling for Notions Clefs box */
    .custom-info-box {
        border: 2px solid #2323FF; /* Bleu DSFR */
        padding: 1rem 1.5rem;
        border-radius: 8px;
        background-color: #f0f4ff; /* Fond bleu clair */
        margin-bottom: 20px;
        font-family: Arial, sans-serif;
        color: #000;
    }
    .custom-info-box h3 {
        color: #2323FF; /* Bleu DSFR */
        font-weight: 700;
        margin-bottom: 10px;
        font-size: 1.3rem;
    }
    .custom-info-box ul {
        padding-left: 20px; /* Conserve le décalage initial des puces */
        margin: 0;
        list-style-type: disc; /* Remet les puces par défaut */
    }
    .custom-info-box ul li {
        margin-bottom: 8px;
        font-size: 1.1rem;
    }

    /* Style spécifique pour la liste imbriquée */
    .custom-info-box ul ul {
        margin-top: 5px; /* Petit espace au-dessus de la sous-liste */
        margin-bottom: 5px; /* Petit espace en dessous de la sous-liste */
        list-style-type: "- "; /* Puces en tiret pour la sous-liste */
        padding-left: 20px; /* Décalage supplémentaire pour la sous-liste */
    }
    .custom-info-box ul ul li {
        font-size: 1rem; /* Taille de police légèrement plus petite pour la sous-liste */
        color: #333; /* Couleur de texte légèrement différente si désiré */
    }


    /* Style for page links */
    .stPageLink {
        margin-bottom: 12px !important;
    }
    /* Make the link text larger and semi-bold */
    .stPageLink p {
        font-size: 1.2rem !important;
        font-weight: 500 !important;
    }
    </style>

    <div class="custom-info-box">
        <h3>Notions clefs</h3>
        <ul>
            <li><b>EvalAP</b> fonctionne avec la logique d'Experiment_set.</li>
            <li>Un Experiment_set regroupe plusieurs experimentations associées à une même analyse (par exemple, la recherche du meilleur prompt system sur votre cas d'usage).</li>
            <li>Pour lancer une experimentation il vous faut :
                <ul>
                    <li> un dataset produit (vous pouvez en importer un sur votre cas d'usage ou sélectionner parmis ceux déjà disponibles).</li>
                    <li> les métriques qui vous servirons dans la prise de décisions</li>
                    <li> les modèles / systèmes IA que vous voulez analyser</li>
                </ul>
            </li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("")

for route in ROUTES:
    if route["id"] in ["home"] or route.get("is_hidden"):
        continue
    st.page_link(route["path"], label=f"{route['title']}: {route['description']}", icon=route["icon"])
    # card(
    #    title= route['title'],
    #    text=route['description'],
    # )


st.markdown("Explore [our documentation](/doc) for more information.")