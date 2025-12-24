import streamlit as st
import pandas as pd
import plotly.express as px

def run():
    st.title("Scénarios financiers & analyse de sensibilité")

    st.markdown("### Choix du scénario")
    scenario = st.radio("Sélectionner un scénario", ["Central", "Optimiste", "Pessimiste"], horizontal=True)

    # Hypothèses de base
    CA_base = st.number_input("Chiffre d'affaires de base", value=500000)
    charges_base = st.number_input("Charges totales de base", value=350000)

    # Coefficients par scénario
    coefficients = {"Central": 1.0, "Optimiste": 1.15, "Pessimiste": 0.85}
    coef = coefficients[scenario]

    # Sliders de sensibilité
    st.markdown("### Sensibilité des hypothèses")
    sens_CA = st.slider("Variation du CA (%)", -30, 30, 0)
    sens_charges = st.slider("Variation des charges (%)", -20, 20, 0)

    CA_scenario = CA_base * coef * (1 + sens_CA / 100)
    charges_scenario = charges_base * (1 + sens_charges / 100)
    resultat = CA_scenario - charges_scenario

    df_scenario = pd.DataFrame({"Indicateur": ["Chiffre d'affaires", "Charges", "Résultat"],
                                "Montant": [CA_scenario, charges_scenario, resultat]})

    st.subheader(f"Résultats – Scénario {scenario}")
    st.dataframe(df_scenario.style.format({"Montant": "{:,.0f}"}))

    # Comparaison multi-scénarios
    df_compare = pd.DataFrame({
        "Scénario": ["Pessimiste", "Central", "Optimiste"],
        "CA": [CA_base*coefficients["Pessimiste"], CA_base, CA_base*coefficients["Optimiste"]],
        "Résultat": [CA_base*coefficients["Pessimiste"]-charges_base, CA_base-charges_base, CA_base*coefficients["Optimiste"]-charges_base]
    })

    fig = px.bar(df_compare, x="Scénario", y="Résultat", color="Scénario", title="Comparaison des résultats par scénario")
    st.plotly_chart(fig, use_container_width=True)
