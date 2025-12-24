import streamlit as st
import pandas as pd
import plotly.express as px

def run():
    st.title("Seuil de rentabilité")

    hyp = st.session_state.get("hypotheses", {})

    st.subheader("Hypothèses")
    CA = st.number_input("Chiffre d'affaires HT", value=500000)
    CV = st.slider("Charges variables (CV)", 0, CA, int(0.4 * CA))
    CF = st.slider("Charges fixes (CF)", 0, CA, int(0.3 * CA))

    MCV = CA - CV
    taux_mcv = MCV / CA if CA != 0 else 0
    seuil = CF / taux_mcv if taux_mcv != 0 else 0

    df = pd.DataFrame({
        "Indicateur": ["CA", "CV", "CF", "MCV", "Taux de MCV", "Seuil de rentabilité"],
        "Valeur": [CA, CV, CF, MCV, taux_mcv * 100, seuil]
    })

    st.dataframe(df)

    # Graphique
    df_graph = pd.DataFrame({
        "Type": ["Seuil de rentabilité", "Chiffre d'affaires"],
        "Montant": [seuil, CA]
    })

    fig = px.bar(df_graph, x="Type", y="Montant", title="CA vs Seuil de rentabilité")
    st.plotly_chart(fig)
