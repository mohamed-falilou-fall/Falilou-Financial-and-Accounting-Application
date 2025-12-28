# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from database import save_module_data, load_module_data

def run():
    st.title("PLAN DE FINANCEMENT (3 ANS)")

    if "plan_financement" not in st.session_state:
        st.session_state["plan_financement"] = load_module_data("plan_financement", "global") or {}

    data = st.session_state["plan_financement"]
    hyp = st.session_state.get("hypotheses", {})
    bfr_module = st.session_state.get("bfr", {})
    cr_module = st.session_state.get("compte_resultat", {})

    annees = ["Année 1", "Année 2", "Année 3"]
    resultats = {}

    with st.form("form_pf"):
        for annee in annees:
            st.subheader(annee)

            emplois = st.number_input(
                "Total des emplois",
                value=data.get(f"emplois_{annee}", 0.0),
                format="%.3f",
                key=f"emplois_{annee}"
            )

            ressources = st.number_input(
                "Total des ressources",
                value=data.get(f"ressources_{annee}", 0.0),
                format="%.3f",
                key=f"ressources_{annee}"
            )

            diff = ressources - emplois
            resultats[annee] = diff

        submitted = st.form_submit_button("Enregistrer")

        if submitted:
            for annee in annees:
                data[f"emplois_{annee}"] = st.session_state[f"emplois_{annee}"]
                data[f"ressources_{annee}"] = st.session_state[f"ressources_{annee}"]
                data[f"diff_{annee}"] = resultats[annee]

            save_module_data("plan_financement", "global", data)
            st.success("Plan de financement enregistré")

    df = pd.DataFrame({
        "Rubrique": ["Total emplois", "Total ressources", "Différence"],
        "Année 1": [data.get("emplois_Année 1",0), data.get("ressources_Année 1",0), data.get("diff_Année 1",0)],
        "Année 2": [data.get("emplois_Année 2",0), data.get("ressources_Année 2",0), data.get("diff_Année 2",0)],
        "Année 3": [data.get("emplois_Année 3",0), data.get("ressources_Année 3",0), data.get("diff_Année 3",0)]
    })

    st.dataframe(df.style.format("{:,.3f} F CFA"))

    if st.button("Imprimer la page"):
        st.table(df)
        st.markdown("<script>window.print();</script>", unsafe_allow_html=True)
