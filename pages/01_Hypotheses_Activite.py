# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

def run():
    st.title("Hypothèses d'activité - Application Financière")

    # Initialisation des données
    if 'hypotheses' not in st.session_state:
        st.session_state['hypotheses'] = {
            "Panier moyen / jour": 50,
            "Nombre de clients / jour": 20,
            "Nombre de jours d’ouverture / semaine": 6,
            "Nombre de jours d’ouverture / an": 312,
            "Salaires individuels": 2000,
            "Salaires employés": 5000,
            "Stock": 10000,
            "Loyer": 1500
        }

    # Formulaire interactif
    with st.form("form_hypotheses"):
        st.header("Saisie des hypothèses")
        panier = st.number_input("Panier moyen / jour (XOF)", value=st.session_state['hypotheses']["Panier moyen / jour"])
        clients = st.number_input("Nombre de clients / jour", value=st.session_state['hypotheses']["Nombre de clients / jour"])
        jours_semaine = st.number_input("Jours d’ouverture / semaine", value=st.session_state['hypotheses']["Nombre de jours d’ouverture / semaine"])
        jours_an = st.number_input("Jours d’ouverture / an", value=st.session_state['hypotheses']["Nombre de jours d’ouverture / an"])
        salaire_indiv = st.number_input("Salaires prélevés à titre individuel (XOF)", value=st.session_state['hypotheses']["Salaires individuels"])
        salaires_emp = st.number_input("Salaires employés (XOF)", value=st.session_state['hypotheses']["Salaires employés"])
        stock = st.number_input("Stock (XOF)", value=st.session_state['hypotheses']["Stock"])
        loyer = st.number_input("Loyer local (XOF)", value=st.session_state['hypotheses']["Loyer"])

        submitted = st.form_submit_button("Enregistrer")
        if submitted:
            st.session_state['hypotheses'].update({
                "Panier moyen / jour": panier,
                "Nombre de clients / jour": clients,
                "Nombre de jours d’ouverture / semaine": jours_semaine,
                "Nombre de jours d’ouverture / an": jours_an,
                "Salaires individuels": salaire_indiv,
                "Salaires employés": salaires_emp,
                "Stock": stock,
                "Loyer": loyer
            })
            st.success("Hypothèses mises à jour !")

    # Calcul du CA HT
    CA_HT = panier * clients * jours_an
    st.metric("Chiffre d'affaires HT (Année 1)", f"{CA_HT:,.2f} XOF")
