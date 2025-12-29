# -*- coding: utf-8 -*-
import streamlit as st
from database import save_module_data  # <-- import de la fonction de sauvegarde

def run():
    st.title("HYPOTHÈSES D'ACTIVITÉ")
    st.subheader("Hypothèses de base – Année 1")

    # =========================
    # INITIALISATION
    # =========================
    if "hypotheses" not in st.session_state:
        st.session_state["hypotheses"] = {
            "panier": 50.000,
            "clients": 20.000,
            "jours_an": 312.000,
            "ca_ht": 0.000,
            "salaires_indiv": 2000.000,
            "salaires_emp": 5000.000,
            "stock": 10000.000,
            "loyer": 1500.000
        }

    h = st.session_state["hypotheses"]

    with st.form("form_hypotheses"):
        st.header("Saisie des hypothèses")

        panier = st.number_input(
            "Panier moyen / jour",
            value=h["panier"],
            format="%.3f"
        )

        clients = st.number_input(
            "Nombre de clients / jour",
            value=h["clients"],
            format="%.3f"
        )

        jours_an = st.number_input(
            "Nombre de jours d’ouverture / an",
            value=h["jours_an"],
            format="%.3f"
        )

        # =========================
        # CALCUL CA
        # =========================
        ca_ht = panier * clients * jours_an

        st.number_input(
            "Chiffre d'affaires HT annuel",
            value=ca_ht,
            format="%.3f",
            disabled=True
        )

        salaires_indiv = st.number_input(
            "Salaires prélevés à titre individuel",
            value=h["salaires_indiv"],
            format="%.3f"
        )

        salaires_emp = st.number_input(
            "Salaires des salariés",
            value=h["salaires_emp"],
            format="%.3f"
        )

        stock = st.number_input(
            "Stock moyen",
            value=h["stock"],
            format="%.3f"
        )

        loyer = st.number_input(
            "Loyer annuel",
            value=h["loyer"],
            format="%.3f"
        )

        submitted = st.form_submit_button("Enregistrer")

        if submitted:
            # =========================
            # MISE À JOUR SESSION
            # =========================
            st.session_state["hypotheses"].update({
                "panier": panier,
                "clients": clients,
                "jours_an": jours_an,
                "ca_ht": ca_ht,
                "salaires_indiv": salaires_indiv,
                "salaires_emp": salaires_emp,
                "stock": stock,
                "loyer": loyer
            })

            # =========================
            # SAUVEGARDE AUTOMATIQUE EN BASE
            # =========================
            save_module_data(
                module="hypotheses",
                annee="1",
                data=st.session_state["hypotheses"]
            )

            st.success("Hypothèses enregistrées avec succès")

    # =========================
    # BOUTON IMPRIMER LA PAGE
    # =========================
    if st.button("Imprimer la page"):
        st.write("<script>window.print();</script>", unsafe_allow_html=True)
