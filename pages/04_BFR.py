# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from database import save_module_data, load_module_data

def run():
    st.title("BESOIN EN FONDS DE ROULEMENT (BFR)")

    if "bfr" not in st.session_state:
        st.session_state["bfr"] = load_module_data("bfr", "global") or {}

    data = st.session_state["bfr"]
    hyp = st.session_state.get("hypotheses", {})

    with st.form("form_bfr"):
        CA = st.number_input("Chiffre d'affaires",
            value=data.get("CA", hyp.get("ca_ht", 0.0)), format="%.3f")

        stock = st.number_input("Stock moyen", value=data.get("stock", 0.0), format="%.3f")
        clients = st.number_input("Créances clients", value=data.get("clients", 0.0), format="%.3f")
        fournisseurs = st.number_input("Dettes fournisseurs", value=data.get("fournisseurs", 0.0), format="%.3f")

        submit = st.form_submit_button("Enregistrer")

        if submit:
            data.update({
                "CA": CA,
                "stock": stock,
                "clients": clients,
                "fournisseurs": fournisseurs
            })
            save_module_data("bfr", "global", data)
            st.success("BFR enregistré")

    BFR = stock + clients - fournisseurs

    df = pd.DataFrame({
        "Rubrique": ["Stock", "Clients", "Fournisseurs", "BFR"],
        "Montant": [stock, clients, fournisseurs, BFR]
    })

    st.dataframe(df.style.format("{:,.3f} F CFA"))

    if st.button("Imprimer la page"):
        st.table(df)
        st.markdown("<script>window.print();</script>", unsafe_allow_html=True)
