import streamlit as st
import pandas as pd

def run():
    st.title("Données financières clés")

    RN = st.number_input("Résultat net", value=60000)
    amortissements = st.number_input("Dotations aux amortissements", value=20000)
    reprises = st.number_input("Reprises", value=5000)

    CAF = RN + amortissements - reprises

    VA = st.number_input("Valeur ajoutée", value=150000)
    rentabilite = RN / VA if VA != 0 else 0

    df = pd.DataFrame({
        "Indicateur": ["Résultat net", "Capacité d'autofinancement", "Valeur ajoutée", "Rentabilité d'exploitation"],
        "Valeur": [RN, CAF, VA, rentabilite * 100]
    })

    st.dataframe(df)

    st.metric("CAF", f"{CAF:,.0f}")
    st.metric("Rentabilité d'exploitation", f"{rentabilite*100:.2f} %")
