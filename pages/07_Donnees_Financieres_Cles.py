# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from database import save_module_data, load_module_data

def run():
    st.title("DONNÉES FINANCIÈRES CLÉS")

    if "donnees_cles" not in st.session_state:
        st.session_state["donnees_cles"] = load_module_data("donnees_cles", "global") or {}

    data = st.session_state["donnees_cles"]

    with st.form("form_donnees_cles"):
        FR = st.number_input("Fonds de roulement (FR)", value=data.get("FR", 0.0), format="%.3f")
        BFR = st.number_input("Besoin en fonds de roulement (BFR)", value=data.get("BFR", 0.0), format="%.3f")
        RN = st.number_input("Résultat net", value=data.get("RN", 0.0), format="%.3f")
        VA = st.number_input("Valeur ajoutée", value=data.get("VA", 0.0), format="%.3f")

        CAF = RN
        tresorerie = FR - BFR
        rentabilite = RN / VA if VA != 0 else 0

        submitted = st.form_submit_button("Enregistrer")

        if submitted:
            data.update({
                "FR": FR,
                "BFR": BFR,
                "RN": RN,
                "VA": VA,
                "CAF": CAF,
                "Tresorerie": tresorerie,
                "Rentabilite": rentabilite * 100
            })

            save_module_data("donnees_cles", "global", data)
            st.success("Données financières enregistrées")

    df = pd.DataFrame({
        "Indicateur": [
            "Fonds de roulement",
            "BFR",
            "Trésorerie",
            "Résultat net",
            "CAF",
            "Rentabilité (%)"
        ],
        "Valeur": [
            data.get("FR",0),
            data.get("BFR",0),
            data.get("Tresorerie",0),
            data.get("RN",0),
            data.get("CAF",0),
            data.get("Rentabilite",0)
        ]
    })

    st.dataframe(df.style.format("{:,.3f}"))

    if st.button("Imprimer la page"):
        st.table(df)
        st.markdown("<script>window.print();</script>", unsafe_allow_html=True)
