import streamlit as st
from pathlib import Path
import importlib.util

# ==============================
# CONFIGURATION
# ==============================
st.set_page_config(
    page_title="Application Financière – Planification Stratégique",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# THEME COULEUR JAUNE MOUTARDE
# ==============================
st.markdown(
    """
    <style>
    /* Couleur du sidebar */
    .css-1d391kg {background-color: #d4af37 !important;}
    /* Couleur du titre principal */
    .stApp h1 {color: #d4af37;}
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================
# SESSION STATE
# ==============================
if "scenario" not in st.session_state:
    st.session_state.scenario = "Central"

# ==============================
# TITRE
# ==============================
st.title("Application Financière de Planification Stratégique et Comptable")
st.caption("Auteur : Mohamed Falilou Fall")

# ==============================
# NAVIGATION
# ==============================
pages = {
    "Hypothèses d’activité": "01_Hypotheses_Activite.py",
    "Compte de résultat": "02_Compte_Resultat_Previsionnel.py",
    "Seuil de rentabilité": "03_Seuil_Rentabilite.py",
    "BFR": "04_BFR.py",
    "Plan de financement": "05_Plan_Financement.py",
    "Plan de trésorerie": "06_Plan_Tresorerie.py",
    "Données financières clés": "07_Donnees_Financieres_Cles.py",
    "Scénarios": "08_Scenarios.py",
    "Export & reporting": "09_Export.py",
}

# ==============================
# SIDEBAR
# ==============================
selection = st.sidebar.radio("Choisir un module", list(pages.keys()))

# ==============================
# CHARGEMENT SÉCURISÉ DES PAGES
# ==============================
BASE_DIR = Path(__file__).parent
PAGE_DIR = BASE_DIR / "pages"
page_path = PAGE_DIR / pages[selection]

if page_path.exists():
    spec = importlib.util.spec_from_file_location("page_module", page_path)
    page_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(page_module)

    if hasattr(page_module, "run"):
        page_module.run()
    else:
        st.error(f"La page {page_path.name} ne contient pas de fonction run()")
else:
    st.error(f"Fichier introuvable : {page_path}")
