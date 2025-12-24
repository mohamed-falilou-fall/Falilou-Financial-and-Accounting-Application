import streamlit as st
import pandas as pd
import plotly.express as px

def run():
    st.title("Besoin en Fonds de Roulement (BFR)")

    CA = st.number_input("Chiffre d'affaires annuel", value=500000)

    st.subheader("Délais (en mois)")
    delai_clients = st.slider("Délai clients", 0.0, 12.0, 2.0)
    delai_fournisseurs = st.slider("Délai fournisseurs", 0.0, 12.0, 1.5)
    stock_mois = st.slider("Stock moyen", 0.0, 12.0, 1.0)

    creances_clients = CA * delai_clients / 12
    dettes_fournisseurs = CA * delai_fournisseurs / 12
    stock = CA * stock_mois / 12

    BFR = creances_clients + stock - dettes_fournisseurs

    df = pd.DataFrame({
        "Poste": ["Créances clients", "Stock", "Dettes fournisseurs", "BFR"],
        "Montant": [creances_clients, stock, -dettes_fournisseurs, BFR]
    })

    st.dataframe(df)

    fig = px.bar(df, x="Poste", y="Montant", title="Structure du BFR")
    st.plotly_chart(fig)
