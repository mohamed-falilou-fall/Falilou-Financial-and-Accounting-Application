# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

def calcul_compte_resultat(CA, achats, loyer, honoraires, publicite,
                           credit_bail, autres_charges, salaires,
                           impots_taxes, amortissements, provisions,
                           frais_financiers, produits_financiers,
                           impots_benef, dividendes):

    marge_brute = CA - achats

    valeur_ajoutee = (
        marge_brute
        - loyer
        - honoraires
        - publicite
        - credit_bail
        - autres_charges
    )

    ebe = valeur_ajoutee - salaires - impots_taxes
    rex = ebe - amortissements - provisions
    rcai = rex - frais_financiers + produits_financiers
    resultat_net = rcai - impots_benef - dividendes
    caf = resultat_net + amortissements + provisions

    return [
        CA, 0, CA,
        achats, marge_brute,
        loyer, honoraires, publicite, credit_bail, autres_charges,
        valeur_ajoutee,
        salaires, impots_taxes,
        ebe,
        amortissements, provisions,
        rex,
        frais_financiers, produits_financiers,
        rcai,
        impots_benef, dividendes,
        resultat_net,
        caf
    ]


def run():
    st.title("COMPTE DE RÉSULTAT PRÉVISIONNEL (3 ANS)")

    hyp = st.session_state.get("hypotheses", {})

    st.info("Les données de l’Année 1 sont pré-alimentées depuis les hypothèses.")

    annees = ["Année 1", "Année 2", "Année 3"]
    resultats = {}

    for annee in annees:
        st.subheader(annee)

        CA = st.number_input(
            "Chiffre d'affaires HT",
            value=hyp.get("ca_ht", 0.0) if annee == "Année 1" else 0.0,
            format="%.3f",
            key=f"ca_{annee}"
        )

        achats = st.number_input("Achats / stock", 0.0, format="%.3f", key=f"ach_{annee}")
        loyer = st.number_input(
            "Loyer",
            hyp.get("loyer", 0.0) if annee == "Année 1" else 0.0,
            format="%.3f",
            key=f"loy_{annee}"
        )
        honoraires = st.number_input("Honoraires", 0.0, format="%.3f", key=f"hon_{annee}")
        publicite = st.number_input("Publicité", 0.0, format="%.3f", key=f"pub_{annee}")
        credit_bail = st.number_input("Crédit-bail", 0.0, format="%.3f", key=f"cb_{annee}")
        autres_charges = st.number_input("Autres charges", 0.0, format="%.3f", key=f"aut_{annee}")

        salaires = st.number_input(
            "Salaires",
            hyp.get("salaires_indiv", 0.0) + hyp.get("salaires_emp", 0.0)
            if annee == "Année 1" else 0.0,
            format="%.3f",
            key=f"sal_{annee}"
        )

        impots_taxes = st.number_input("Impôts & taxes", 0.0, format="%.3f", key=f"it_{annee}")
        amortissements = st.number_input("Amortissements", 0.0, format="%.3f", key=f"am_{annee}")
        provisions = st.number_input("Provisions", 0.0, format="%.3f", key=f"prov_{annee}")
        frais_financiers = st.number_input("Frais financiers", 0.0, format="%.3f", key=f"ff_{annee}")
        produits_financiers = st.number_input("Produits financiers", 0.0, format="%.3f", key=f"pf_{annee}")
        impots_benef = st.number_input("Impôts sur bénéfices", 0.0, format="%.3f", key=f"ib_{annee}")
        dividendes = st.number_input("Dividendes", 0.0, format="%.3f", key=f"div_{annee}")

        resultats[annee] = calcul_compte_resultat(
            CA, achats, loyer, honoraires, publicite,
            credit_bail, autres_charges, salaires,
            impots_taxes, amortissements, provisions,
            frais_financiers, produits_financiers,
            impots_benef, dividendes
        )

    lignes = [
        "Ventes", "Production", "Chiffre d'affaires",
        "Achats", "Marge brute",
        "Loyer", "Honoraires", "Publicité", "Crédit-bail", "Autres charges",
        "Valeur ajoutée",
        "Salaires", "Impôts & taxes",
        "EBE",
        "Amortissements", "Provisions",
        "Résultat d'exploitation",
        "Frais financiers", "Produits financiers",
        "RCAI",
        "Impôts sur bénéfices", "Dividendes",
        "Résultat net",
        "CAF"
    ]

    df = pd.DataFrame({
        "Rubrique": lignes,
        "Année 1": resultats["Année 1"],
        "Année 2": resultats["Année 2"],
        "Année 3": resultats["Année 3"]
    })

    st.subheader("Compte de Résultat Prévisionnel")
    st.dataframe(
        df.style.format({
            "Année 1": "{:,.3f} F CFA",
            "Année 2": "{:,.3f} F CFA",
            "Année 3": "{:,.3f} F CFA"
        })
    )
