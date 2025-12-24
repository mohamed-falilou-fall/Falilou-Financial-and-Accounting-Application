import streamlit as st
import pandas as pd

def run():
    st.title("Compte de Résultat Prévisionnel")

    # Récupérer les hypothèses
    hyp = st.session_state.get('hypotheses', {})
    CA = hyp.get("Panier moyen / jour", 0) * hyp.get("Nombre de clients / jour", 0) * hyp.get("Nombre de jours d’ouverture / an", 0)

    # Structure du compte de résultat simplifié
    data_cr = {
        "Rubrique": [
            "Ventes de marchandises",
            "Production",
            "Chiffre d'affaires (CA)",
            "Achats de marchandises et variation de stock",
            "Marge brute (MB)",
            "Loyer et charges locatives",
            "Honoraires et assurances",
            "Publicité et frais commerciaux",
            "Loyers de crédit bail",
            "Fournitures et autres charges",
            "Valeur ajoutée (VA)",
            "Salaires et charges sociales",
            "Impôts et Taxes",
            "Excédent brut d'exploitation (EBE)",
            "Dotations aux amortissements",
            "Dotations aux provisions",
            "Résultat d'exploitation (RE)",
            "Frais financiers",
            "Produits financiers",
            "Résultat courant avant impôts (RCAI)",
            "Impôts sur les bénéfices",
            "Dividendes",
            "Résultat net (RN)",
            "Capacité d'autofinancement (CAF)"
        ],
        "Année 1": [
            CA, 0, CA, 0, 0, hyp.get("Loyer",0), 0, 0, 0, 0, 0, hyp.get("Salaires employés",0)+hyp.get("Salaires individuels",0), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ]
    }

    df_cr = pd.DataFrame(data_cr)

    # Calculs automatiques
    df_cr.loc[df_cr["Rubrique"]=="Marge brute (MB)", "Année 1"] = df_cr.loc[df_cr["Rubrique"]=="Chiffre d'affaires (CA)", "Année 1"].values[0] - df_cr.loc[df_cr["Rubrique"]=="Achats de marchandises et variation de stock", "Année 1"].values[0]
    df_cr.loc[df_cr["Rubrique"]=="Valeur ajoutée (VA)", "Année 1"] = df_cr.loc[df_cr["Rubrique"]=="Marge brute (MB)", "Année 1"].values[0] - sum(df_cr.loc[df_cr["Rubrique"].isin([
        "Loyer et charges locatives", "Honoraires et assurances", "Publicité et frais commerciaux", "Loyers de crédit bail", "Fournitures et autres charges"
    ]), "Année 1"])
    df_cr.loc[df_cr["Rubrique"]=="Excédent brut d'exploitation (EBE)", "Année 1"] = df_cr.loc[df_cr["Rubrique"]=="Valeur ajoutée (VA)", "Année 1"].values[0] - df_cr.loc[df_cr["Rubrique"]=="Salaires et charges sociales", "Année 1"].values[0]
    df_cr.loc[df_cr["Rubrique"]=="Résultat net (RN)", "Année 1"] = df_cr.loc[df_cr["Rubrique"]=="Excédent brut d'exploitation (EBE)", "Année 1"].values[0]

    # Affichage du tableau
    st.dataframe(df_cr.style.format({"Année 1": "{:,.2f} XOF"}))
