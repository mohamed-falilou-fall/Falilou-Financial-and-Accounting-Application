# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from database import save_module_data, load_module_data

def run():
    st.title("PLAN DE TRÉSORERIE (3 ANS)")

    if "tresorerie" not in st.session_state:
        st.session_state["tresorerie"] = load_module_data("tresorerie", "global") or {}

    data = st.session_state["tresorerie"]
    annees = ["Année 1", "Année 2", "Année 3"]

    with st.form("form_treso"):
        for annee in annees:
            st.subheader(annee)

            entrees = st.number_input(
                "Total entrées",
                value=data.get(f"entrees_{annee}", 0.0),
                format="%.3f",
                key=f"entrees_{annee}"
            )

            sorties = st.number_input(
                "Total sorties",
                value=data.get(f"sorties_{annee}", 0.0),
                format="%.3f",
                key=f"sorties_{annee}"
            )

            solde_debut = st.number_input(
                "Solde début",
                value=data.get(f"solde_debut_{annee}", 0.0),
                format="%.3f",
                key=f"solde_debut_{annee}"
            )

            solde_fin = solde_debut + entrees - sorties
            st.markdown(f"**Solde fin : {solde_fin:,.3f} F CFA**")

            data[f"solde_fin_{annee}"] = solde_fin

        submitted = st.form_submit_button("Enregistrer")

        if submitted:
            save_module_data("tresorerie", "global", data)
            st.success("Plan de trésorerie enregistré")

    df = pd.DataFrame({
        "Rubrique": ["Entrées", "Sorties", "Solde fin"],
        "Année 1": [data.get("entrees_Année 1",0), data.get("sorties_Année 1",0), data.get("solde_fin_Année 1",0)],
        "Année 2": [data.get("entrees_Année 2",0), data.get("sorties_Année 2",0), data.get("solde_fin_Année 2",0)],
        "Année 3": [data.get("entrees_Année 3",0), data.get("sorties_Année 3",0), data.get("solde_fin_Année 3",0)]
    })

    st.dataframe(df.style.format("{:,.3f} F CFA"))

    if st.button("Imprimer la page"):
        st.table(df)
        st.markdown("<script>window.print();</script>", unsafe_allow_html=True)
