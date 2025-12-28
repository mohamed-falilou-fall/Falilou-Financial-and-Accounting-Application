# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from database import save_module_data, load_module_data

def calcul_compte_resultat(CA, achats, loyer, honoraires, publicite,
                           credit_bail, autres_charges, salaires,
                           impots_taxes, amortissements, provisions,
                           frais_financiers, produits_financiers,
                           impots_benef, dividendes):

    marge_brute = CA - achats
    valeur_ajoutee = marge_brute - loyer - honoraires - publicite - credit_bail - autres_charges
    ebe = valeur_ajoutee - salaires - impots_taxes
    rex = ebe - amortissements - provisions
    rcai = rex - frais_financiers + produits_financiers
    resultat_net = rcai - impots_benef - dividendes
    caf = resultat_net + amortissements + provisions

    return resultat_net, caf


def run():
    st.title("COMPTE DE RÉSULTAT PRÉVISIONNEL (3 ANS)")

    # =========================
    # CHARGEMENT DB
    # =========================
    if "compte_resultat" not in st.session_state:
        st.session_state["compte_resultat"] = load_module_data("compte_resultat", "global") or {}

    hyp = st.session_state.get("hypotheses", {})
    data = st.session_state["compte_resultat"]

    annees = ["Année 1", "Année 2", "Année 3"]
    tableau = {}

    with st.form("form_cr"):
        for annee in annees:
            st.subheader(annee)

            CA = st.number_input("Chiffre d'affaires HT",
                value=data.get(f"ca_{annee}", hyp.get("ca_ht", 0.0) if annee=="Année 1" else 0.0),
                format="%.3f", key=f"ca_{annee}")

            achats = st.number_input("Achats", value=data.get(f"ach_{annee}", 0.0), format="%.3f", key=f"ach_{annee}")
            loyer = st.number_input("Loyer", value=data.get(f"loy_{annee}", hyp.get("loyer",0.0) if annee=="Année 1" else 0.0),
                format="%.3f", key=f"loy_{annee}")

            honoraires = st.number_input("Honoraires", value=data.get(f"hon_{annee}", 0.0), format="%.3f", key=f"hon_{annee}")
            publicite = st.number_input("Publicité", value=data.get(f"pub_{annee}", 0.0), format="%.3f", key=f"pub_{annee}")
            credit_bail = st.number_input("Crédit-bail", value=data.get(f"cb_{annee}", 0.0), format="%.3f", key=f"cb_{annee}")
            autres_charges = st.number_input("Autres charges", value=data.get(f"aut_{annee}", 0.0), format="%.3f", key=f"aut_{annee}")

            salaires = st.number_input("Salaires",
                value=data.get(f"sal_{annee}", hyp.get("salaires_indiv",0)+hyp.get("salaires_emp",0) if annee=="Année 1" else 0.0),
                format="%.3f", key=f"sal_{annee}")

            impots = st.number_input("Impôts & taxes", value=data.get(f"it_{annee}", 0.0), format="%.3f", key=f"it_{annee}")
            amort = st.number_input("Amortissements", value=data.get(f"am_{annee}", 0.0), format="%.3f", key=f"am_{annee}")
            prov = st.number_input("Provisions", value=data.get(f"prov_{annee}", 0.0), format="%.3f", key=f"prov_{annee}")
            ff = st.number_input("Frais financiers", value=data.get(f"ff_{annee}", 0.0), format="%.3f", key=f"ff_{annee}")
            pf = st.number_input("Produits financiers", value=data.get(f"pf_{annee}", 0.0), format="%.3f", key=f"pf_{annee}")
            ib = st.number_input("Impôts sur bénéfices", value=data.get(f"ib_{annee}", 0.0), format="%.3f", key=f"ib_{annee}")
            div = st.number_input("Dividendes", value=data.get(f"div_{annee}", 0.0), format="%.3f", key=f"div_{annee}")

            rn, caf = calcul_compte_resultat(CA, achats, loyer, honoraires, publicite,
                                             credit_bail, autres_charges, salaires,
                                             impots, amort, prov, ff, pf, ib, div)

            tableau[annee] = {"Résultat net": rn, "CAF": caf}

        submit = st.form_submit_button("Enregistrer")

        if submit:
            for k in st.session_state:
                if "_" in k:
                    data[k] = st.session_state[k]

            save_module_data("compte_resultat", "global", data)
            st.success("Compte de résultat enregistré")

    df = pd.DataFrame(tableau)
    st.dataframe(df.style.format("{:,.3f} F CFA"))

    if st.button("Imprimer la page"):
        st.table(df)
        st.markdown("<script>window.print();</script>", unsafe_allow_html=True)
