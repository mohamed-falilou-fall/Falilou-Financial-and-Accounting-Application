import streamlit as st
import pandas as pd
import plotly.express as px

def run():
    st.title("Plan de trésorerie")

    mois = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sept", "Oct", "Nov", "Déc"]

    st.subheader("Entrées mensuelles")
    entrees = [st.number_input(f"Entrées {m}", value=40000) for m in mois]

    st.subheader("Sorties mensuelles")
    sorties = [st.number_input(f"Sorties {m}", value=35000) for m in mois]

    solde = []
    cumul = 0
    for e, s in zip(entrees, sorties):
        cumul += e - s
        solde.append(cumul)

    df = pd.DataFrame({
        "Mois": mois,
        "Trésorerie cumulée": solde
    })

    fig = px.line(df, x="Mois", y="Trésorerie cumulée", title="Évolution de la trésorerie cumulée")
    st.plotly_chart(fig)
