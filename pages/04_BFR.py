# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

def run():
    st.title("Besoin en Fonds de Roulement (BFR)")

    hyp = st.session_state.get("hypotheses", {})

    annees = ["Année 1", "Année 2", "Année 3"]
    resultats = {}

    for annee in annees:
        st.subheader(annee)

        # =========================
        # Chiffre d'affaires HT
        # =========================
        CA = st.number_input(
            "Chiffre d'affaires HT",
            value=hyp.get("Chiffre d'affaires HT (1 x 2 x 3)", 0.0) if annee=="Année 1" else 0.0,
            format="%.3f",
            key=f"ca_bfr_{annee}"
        )

        st.markdown("**Stocks et délais**")
        achats_pct_CA = st.number_input(
            "Achats consommés + sous-traitance (% du CA HT)",
            value=60.0 if annee=="Année 1" else 0.0,
            format="%.3f",
            key=f"achats_pct_{annee}"
        ) / 100.0

        delai_fournisseurs = st.slider(
            "Délai moyen paiement fournisseurs (mois)",
            0.0, 12.0, 1.5,
            key=f"delai_fournisseurs_{annee}"
        )

        stock_matieres = st.slider(
            "Stock matières premières (mois d'achat)",
            0.0, 12.0, 1.0,
            key=f"stock_matieres_{annee}"
        )

        stock_encours = st.slider(
            "Stock produits en cours (mois de cycle fabrication)",
            0.0, 12.0, 0.5,
            key=f"stock_encours_{annee}"
        )

        stock_finis = st.slider(
            "Stock produits finis (mois de vente)",
            0.0, 12.0, 0.5,
            key=f"stock_finis_{annee}"
        )

        delai_clients = st.slider(
            "Délai moyen règlement clients (mois)",
            0.0, 12.0, 2.0,
            key=f"delai_clients_{annee}"
        )

        # =========================
        # Calculs
        # =========================
        achats = CA * achats_pct_CA

        stock_montants = {
            "Stock matières": achats * stock_matieres / 12,
            "Produits en cours": achats * stock_encours / 12,
            "Produits finis": CA * stock_finis / 12
        }

        total_stock = sum(stock_montants.values())
        creances_clients = CA * delai_clients / 12
        dettes_fournisseurs = achats * delai_fournisseurs / 12

        total_emplois = total_stock + creances_clients
        total_ressources = dettes_fournisseurs  # pas d'acomptes clients pour simplification
        BFR = total_emplois - total_ressources

        resultats[annee] = {
            "Stock matières": stock_montants["Stock matières"],
            "Produits en cours": stock_montants["Produits en cours"],
            "Produits finis": stock_montants["Produits finis"],
            "Total stock HT": total_stock,
            "Clients TTC": creances_clients,
            "Total emplois": total_emplois,
            "Fournisseurs TTC": dettes_fournisseurs,
            "Acomptes clients TTC": 0.0,
            "Total ressources": total_ressources,
            "BFR": BFR
        }

    # =========================
    # Tableau final
    # =========================
    df = pd.DataFrame({
        "Rubrique": [
            "Stock matières",
            "Produits en cours",
            "Produits finis",
            "Total stock HT (encours moyen)",
            "Clients TTC (encours moyen)",
            "(1) TOTAL EMPLOIS",
            "Fournisseurs TTC",
            "Acomptes clients TTC",
            "(2) TOTAL RESSOURCES",
            "BESOIN EN FONDS DE ROULEMENT (BFR)"
        ],
        "Année 1": [
            resultats["Année 1"]["Stock matières"],
            resultats["Année 1"]["Produits en cours"],
            resultats["Année 1"]["Produits finis"],
            resultats["Année 1"]["Total stock HT"],
            resultats["Année 1"]["Clients TTC"],
            resultats["Année 1"]["Total emplois"],
            resultats["Année 1"]["Fournisseurs TTC"],
            resultats["Année 1"]["Acomptes clients TTC"],
            resultats["Année 1"]["Total ressources"],
            resultats["Année 1"]["BFR"]
        ],
        "Année 2": [
            resultats["Année 2"]["Stock matières"],
            resultats["Année 2"]["Produits en cours"],
            resultats["Année 2"]["Produits finis"],
            resultats["Année 2"]["Total stock HT"],
            resultats["Année 2"]["Clients TTC"],
            resultats["Année 2"]["Total emplois"],
            resultats["Année 2"]["Fournisseurs TTC"],
            resultats["Année 2"]["Acomptes clients TTC"],
            resultats["Année 2"]["Total ressources"],
            resultats["Année 2"]["BFR"]
        ],
        "Année 3": [
            resultats["Année 3"]["Stock matières"],
            resultats["Année 3"]["Produits en cours"],
            resultats["Année 3"]["Produits finis"],
            resultats["Année 3"]["Total stock HT"],
            resultats["Année 3"]["Clients TTC"],
            resultats["Année 3"]["Total emplois"],
            resultats["Année 3"]["Fournisseurs TTC"],
            resultats["Année 3"]["Acomptes clients TTC"],
            resultats["Année 3"]["Total ressources"],
            resultats["Année 3"]["BFR"]
        ]
    })

    st.subheader("Tableau BFR")
    st.dataframe(df.style.format({
        "Année 1": "{:,.3f} F CFA",
        "Année 2": "{:,.3f} F CFA",
        "Année 3": "{:,.3f} F CFA"
    }))

    # =========================
    # Graphique
    # =========================
    import plotly.express as px
    
    fig = px.bar(
        df.iloc[-1:],  # uniquement BFR
        x="Rubrique",
        y=["Année 1", "Année 2", "Année 3"],
        title="BFR par année"
    )
    st.plotly_chart(fig)
