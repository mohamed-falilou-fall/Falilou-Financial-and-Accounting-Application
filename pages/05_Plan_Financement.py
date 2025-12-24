import streamlit as st
import pandas as pd

def run():
    st.title("Plan de financement")

    st.subheader("EMPLOIS")
    immobilisations = st.number_input("Immobilisations totales", value=200000)
    bfr = st.number_input("Besoin en fonds de roulement", value=80000)
    dividendes = st.number_input("Dividendes", value=0)

    total_emplois = immobilisations + bfr + dividendes

    st.subheader("RESSOURCES")
    capitaux_propres = st.number_input("Capitaux propres", value=150000)
    emprunts = st.number_input("Emprunts bancaires", value=100000)
    caf = st.number_input("Capacité d'autofinancement", value=30000)

    total_ressources = capitaux_propres + emprunts + caf
    difference = total_ressources - total_emplois

    df = pd.DataFrame({
        "Type": ["Emplois", "Ressources", "Écart"],
        "Montant": [total_emplois, total_ressources, difference]
    })

    st.dataframe(df)

    if difference < 0:
        st.error("Plan de financement déséquilibré")
    else:
        st.success("Plan de financement équilibré")
