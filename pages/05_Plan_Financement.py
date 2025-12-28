# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

def run():
    st.title("Plan de financement")

    hyp = st.session_state.get("hypotheses", {})
    bfr_module = st.session_state.get("bfr", {})  # optionnel si on stocke les résultats de BFR
    cr_module = st.session_state.get("compte_resultat", {})  # optionnel pour CAF

    annees = ["Année 1", "Année 2", "Année 3"]
    resultats = {}

    for annee in annees:
        st.subheader(annee)

        st.markdown("**EMPLOIS**")
        immobilisations_incorporelles = st.number_input("Immobilisations incorporelles HT", value=0.0, format="%.3f", key=f"immobilisations_incorp_{annee}")
        frais_etablissement = st.number_input("Frais de premier établissement", value=0.0, format="%.3f", key=f"frais_etab_{annee}")
        recherche_dev = st.number_input("Recherche et développement", value=0.0, format="%.3f", key=f"rd_{annee}")
        fonds_commerce = st.number_input("Fonds de commerce", value=0.0, format="%.3f", key=f"fonds_commerce_{annee}")
        droit_bail = st.number_input("Droit au bail", value=0.0, format="%.3f", key=f"droit_bail_{annee}")
        immobilisations_corporelles = st.number_input("Immobilisations corporelles HT", value=0.0, format="%.3f", key=f"immobilisations_corp_{annee}")
        terrains = st.number_input("Terrains", value=0.0, format="%.3f", key=f"terrains_{annee}")
        batiments = st.number_input("Bâtiments", value=0.0, format="%.3f", key=f"batiments_{annee}")
        frais_installation = st.number_input("Frais d'installation et d'aménagements", value=0.0, format="%.3f", key=f"frais_install_{annee}")
        materiel_info = st.number_input("Matériel informatique et outillage", value=0.0, format="%.3f", key=f"materiel_info_{annee}")
        materiel_bureau = st.number_input("Matériel de bureau et mobilier", value=0.0, format="%.3f", key=f"materiel_bureau_{annee}")

        # BFR depuis le module BFR si dispo, sinon saisie manuelle
        bfr_val = st.number_input("Besoin en fonds de roulement", 
                                  value=bfr_module.get(annee, {}).get("BFR", 0.0) if bfr_module else 0.0,
                                  format="%.3f",
                                  key=f"bfr_{annee}")

        distribution_dividendes = st.number_input("Distribution de dividendes", value=0.0, format="%.3f", key=f"dividendes_{annee}")
        remboursement_emprunts = st.number_input("Remboursement emprunts (capital)", value=0.0, format="%.3f", key=f"remb_emprunts_{annee}")

        total_emplois = sum([
            immobilisations_incorporelles, frais_etablissement, recherche_dev, fonds_commerce, droit_bail,
            immobilisations_corporelles, terrains, batiments, frais_installation, materiel_info, materiel_bureau,
            bfr_val, distribution_dividendes, remboursement_emprunts
        ])

        st.markdown("**RESSOURCES**")
        capitaux_propres_nature = st.number_input("Capitaux propres en nature", value=0.0, format="%.3f", key=f"capitaux_nature_{annee}")
        capitaux_propres_numeraire = st.number_input("Capitaux propres en numéraire", value=0.0, format="%.3f", key=f"capitaux_num_{annee}")
        subventions = st.number_input("Subventions d'équipement", value=0.0, format="%.3f", key=f"subventions_{annee}")
        comptes_associes = st.number_input("Comptes courants d'associés", value=0.0, format="%.3f", key=f"comptes_associes_{annee}")
        emprunt_bancaire = st.number_input("Emprunt bancaire à MLT", value=0.0, format="%.3f", key=f"emprunt_bancaire_{annee}")

        # CAF depuis module CR si dispo
        caf_val = st.number_input("Capacité d'autofinancement (CAF)", 
                                  value=cr_module.get(annee, {}).get("CAF", 0.0) if cr_module else 0.0,
                                  format="%.3f",
                                  key=f"caf_{annee}")

        total_ressources = sum([
            capitaux_propres_nature, capitaux_propres_numeraire, subventions,
            comptes_associes, emprunt_bancaire, caf_val
        ])

        difference_annuelle = total_ressources - total_emplois

        resultats[annee] = {
            "Total emplois": total_emplois,
            "Total ressources": total_ressources,
            "Différence annuelle": difference_annuelle
        }

    # Calcul différences cumulées
    differences_cumulees = []
    cumul = 0.0
    for annee in annees:
        cumul += resultats[annee]["Différence annuelle"]
        differences_cumulees.append(cumul)

    # =========================
    # Tableau final
    # =========================
    df = pd.DataFrame({
        "Rubrique": ["TOTAL DES BESOINS", "TOTAL DES RESSOURCES", "DIFFERENCES ANNUELLES", "DIFFERENCES CUMULEES"],
        "Année 1": [
            resultats["Année 1"]["Total emplois"],
            resultats["Année 1"]["Total ressources"],
            resultats["Année 1"]["Différence annuelle"],
            differences_cumulees[0]
        ],
        "Année 2": [
            resultats["Année 2"]["Total emplois"],
            resultats["Année 2"]["Total ressources"],
            resultats["Année 2"]["Différence annuelle"],
            differences_cumulees[1]
        ],
        "Année 3": [
            resultats["Année 3"]["Total emplois"],
            resultats["Année 3"]["Total ressources"],
            resultats["Année 3"]["Différence annuelle"],
            differences_cumulees[2]
        ]
    })

    st.subheader("Tableau Plan de Financement")
    st.dataframe(df.style.format({
        "Année 1": "{:,.3f} F CFA",
        "Année 2": "{:,.3f} F CFA",
        "Année 3": "{:,.3f} F CFA"
    }))

    # Message de validation
    if any([resultats[annee]["Différence annuelle"] != 0.0 for annee in annees]):
        st.warning("Attention : le plan de financement n'est pas équilibré pour certaines années.")
    else:
        st.success("Plan de financement équilibré pour toutes les années.")
