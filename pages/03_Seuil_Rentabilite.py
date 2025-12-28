# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from database import save_module_data, load_module_data

def run():
    st.title("SEUIL DE RENTABILITÉ")

    if "seuil_rentabilite" not in st.session_state:
        st.session_state["seuil_rentabilite"] = load_module_data("seuil_rentabilite", "global") or {}

    data = st.session_state["seuil_rentabilite"]
    hyp = st.session_state.get("hypotheses", {})

    with st.form("form_sr"):
        CA = st.number_input("Chiffre d'affaires",
            value=data.get("CA", hyp.get("ca_ht", 0.0)), format="%.3f")

        CV = st.number_input("Charges variables", value=data.get("CV", 0.0), format="%.3f")
        CF = st.number_input("Charges fixes", value=data.get("CF", 0.0), format="%.3f")

        submit = st.form_submit_button("Enregistrer")

        if submit:
            data.update({"CA": CA, "CV": CV, "CF": CF})
            save_module_data("seuil_rentabilite", "global", data)
            st.success("Seuil enregistré")

    taux = (CA - CV) / CA if CA != 0 else 0
    seuil = CF / taux if taux != 0 else 0

    df = pd.DataFrame({
        "Indicateur": ["CA", "Charges variables", "Charges fixes", "Taux MCV", "Seuil"],
        "Valeur": [CA, CV, CF, taux*100, seuil]
    })

    st.dataframe(df.style.format("{:,.3f} F CFA"))

    if st.button("Imprimer la page"):
        st.table(df)
        st.markdown("<script>window.print();</script>", unsafe_allow_html=True)
