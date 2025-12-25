# -*- coding: utf-8 -*-
import streamlit as st
from pathlib import Path
import importlib.util

# ==============================
# CONFIGURATION PAGE
# ==============================
st.set_page_config(
    page_title="Application Financière – Planification Stratégique",
    layout="wide"
)

# ==============================
# STYLE THEME JAUNE MOUTARDE
# ==============================
st.markdown(
    """
    <style>
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #D4A017;  /* jaune moutarde */
    }
    /* Boutons */
    .stButton>button {
        background-color: #D4A017;
        color: white;
    }
    /* Header principal */
    .css-18e3th9 {
        background-color: #FFF8DC;  /* fond clair pour le header */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================
# SESSION STATE INIT
# ==============================
if "scenario" not in st.session_state:
    st.session_state.scenario = "Central"

# ==============================
# TITRE PRINCIPAL
# ==============================
st.title("Application Financière de Planification Stratégique et Comptable")
st.caption("Auteur : Mohamed Falilou Fall")

# ==============================
# DICTIONNAIRE DES PAGES
# ==============================
pages = {
    "01_Hypothèses d’activité": "01_Hypotheses_Activite.py",
    "02_Compte de résultat": "02_Compte_Resultat_Previsionnel.py",
    "03_Seuil de rentabilité": "03_Seuil_Rentabilite.py",
    "04_BFR": "04_BFR.py",
    "05_Plan de financement": "05_Plan_Financement.py",
    "06_Plan de trésorerie": "06_Plan_Tresorerie.py",
    "07_Données financières clés": "07_Donnees_Financieres_Cles.py",
    "08_Scénarios": "08_Scenarios.py",
    "09_Export & reporting": "09_Export.py",
}

# ==============================
# SIDEBAR NAVIGATION
# ==============================
selection = st.sidebar.radio("Choisir un module", list(pages.keys()))

# ==============================
# CHARGEMENT SÉCURISÉ DU MODULE
# ==============================
BASE_DIR = Path(__file__).parent          # dossier où se trouve app.py
PAGE_DIR = BASE_DIR / "pages"             # dossier ./pages

page_path = PAGE_DIR / pages[selection]   # chemin complet vers le script sélectionné

if page_path.exists():
    spec = importlib.util.spec_from_file_location("page_module", page_path)
    page_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(page_module)

    # Vérifie que le module contient la fonction run()
    if hasattr(page_module, "run"):
        page_module.run()
    else:
        st.error(f"La page {page_path.name} ne contient pas de fonction run()")
else:
    st.error(f"Fichier introuvable : {page_path}")
