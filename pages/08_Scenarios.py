# -*- coding: utf-8 -*-

# =========================
# Sécurisation globale matplotlib (sans altérer le code)
# =========================
import matplotlib
matplotlib.use("Agg")

import streamlit as st
import pandas as pd


def run():
    st.title("Scénarios financiers & analyse de sensibilité")

    st.markdown("### Choix du scénario")
    scenario = st.radio(
        "Sélectionner un scénario",
        ["Central", "Optimiste", "Pessimiste"],
        horizontal=True
    )

    # Hypothèses de base depuis session_state
    CA_base = st.session_state.get("hypotheses", {}).get(
        "Chiffre d'affaires HT (1 x 2 x 3)", 0.0
    )
    charges_base = (
        st.session_state
        .get("compte_resultat", {})
        .get("Année 1", {})
        .get("Charges totales", 0.0)
    )

    # Coefficients par scénario
    coefficients = {
        "Central": 1.0,
        "Optimiste": 1.15,
        "Pessimiste": 0.85
    }
    coef = coefficients[scenario]

    # Sliders de sensibilité
    st.markdown("### Sensibilité des hypothèses")
    sens_CA = st.slider("Variation du CA (%)", -30, 30, 0)
    sens_charges = st.slider("Variation des charges (%)", -20, 20, 0)

    CA_scenario = CA_base * coef * (1 + sens_CA / 100)
    charges_scenario = charges_base * (1 + sens_charges / 100)
    resultat = CA_scenario - charges_scenario

    df_scenario = pd.DataFrame({
        "Indicateur": [
            "Chiffre d'affaires",
            "Charges",
            "Résultat"
        ],
        "Montant (F CFA)": [
            CA_scenario,
            charges_scenario,
            resultat
        ]
    })

    st.subheader(f"Résultats – Scénario {scenario}")
    st.dataframe(
        df_scenario.style.format({
            "Montant (F CFA)": "{:,.3f}"
        })
    )

    # =========================
    # Comparaison multi-scénarios
    # =========================
    df_compare = pd.DataFrame({
        "Scénario": ["Pessimiste", "Central", "Optimiste"],
        "CA (F CFA)": [
            CA_base * coefficients["Pessimiste"],
            CA_base,
            CA_base * coefficients["Optimiste"]
        ],
        "Résultat (F CFA)": [
            CA_base * coefficients["Pessimiste"] - charges_base,
            CA_base - charges_base,
            CA_base * coefficients["Optimiste"] - charges_base
        ]
    })

    # =========================
# Graphique simple (Streamlit natif)
# =========================
st.subheader("Comparaison des résultats par scénario")

df_graph = (
    df_compare
    .set_index("Scénario")[["Résultat (F CFA)"]]
)

st.bar_chart(df_graph)

