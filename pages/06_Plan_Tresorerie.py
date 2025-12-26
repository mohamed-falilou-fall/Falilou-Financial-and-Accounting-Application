# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

def run():
    st.title("Plan de Trésorerie (3 ans)")

    mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
            "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

    annees = ["Année 1", "Année 2", "Année 3"]

    # Récupérer CA et BFR depuis session_state si disponibles
    hyp = st.session_state.get("hypotheses", {})
    bfr_module = st.session_state.get("bfr", {})
    cr_module = st.session_state.get("compte_resultat", {})

    for annee in annees:
        st.subheader(annee)

        st.markdown("**ENTRÉES**")
        ca = hyp.get("Chiffre d'affaires HT (1 x 2 x 3)", 0.0)  # CA annuel
        creances = st.number_input(f"Créances clients ({annee})", value=ca * 0.3, format="%.3f", key=f"creances_{annee}")  # Ex : 30% du CA
        capital = st.number_input(f"Capital ({annee})", value=0.0, format="%.3f", key=f"capital_{annee}")
        comptes_courants = st.number_input(f"Comptes courants ({annee})", value=0.0, format="%.3f", key=f"comptes_courants_{annee}")
        primes_subventions = st.number_input(f"Primes et subventions ({annee})", value=0.0, format="%.3f", key=f"primes_{annee}")
        emprunts = st.number_input(f"Emprunts ({annee})", value=0.0, format="%.3f", key=f"emprunts_{annee}")
        autres_produits = st.number_input(f"Autres produits ({annee})", value=0.0, format="%.3f", key=f"autres_produits_{annee}")
        produits_financiers = st.number_input(f"Produits financiers ({annee})", value=cr_module.get(annee, {}).get("CAF", 0.0) if cr_module else 0.0, format="%.3f", key=f"produits_financiers_{annee}")

        total_entrees = sum([creances, capital, comptes_courants, primes_subventions, emprunts, autres_produits, produits_financiers])

        st.markdown("**SORTIES**")
        fournisseurs = st.number_input(f"Fournisseurs ({annee})", value=ca * 0.2, format="%.3f", key=f"fournisseurs_{annee}")  # Ex : 20% du CA
        immobilisations = st.number_input(f"Acquisitions immobilisations ({annee})", value=0.0, format="%.3f", key=f"immobilisations_{annee}")
        remboursements_emprunts = st.number_input(f"Remboursements emprunts ({annee})", value=0.0, format="%.3f", key=f"remb_emprunts_treso_{annee}")
        personnel = st.number_input(f"Personnel ({annee})", value=hyp.get("Salaires prélevés à titre individuel",0.0)+hyp.get("Salaires prélevés pour mes salariés",0.0), format="%.3f", key=f"personnel_{annee}")
        autres_charges = st.number_input(f"Autres charges ({annee})", value=0.0, format="%.3f", key=f"autres_charges_{annee}")
        charges_financieres = st.number_input(f"Charges financières ({annee})", value=0.0, format="%.3f", key=f"charges_fin_{annee}")

        total_sorties = sum([fournisseurs, immobilisations, remboursements_emprunts, personnel, autres_charges, charges_financieres])

        st.markdown("**SOLDES**")
        solde_debut = st.number_input(f"Solde début ({annee})", value=0.0, format="%.3f", key=f"solde_debut_{annee}")
        solde_fin = solde_debut + total_entrees - total_sorties

        st.markdown(f"**Total entrées ({annee}) : {total_entrees:,.3f} F CFA**")
        st.markdown(f"**Total sorties ({annee}) : {total_sorties:,.3f} F CFA**")
        st.markdown(f"**Solde fin ({annee}) : {solde_fin:,.3f} F CFA**")

        # DataFrame récapitulatif
        df = pd.DataFrame({
            "Mois": mois + ["Total"],
            "Entrées": [total_entrees/12]*12 + [total_entrees],
            "Sorties": [total_sorties/12]*12 + [total_sorties],
            "Solde cumulée": [solde_debut + i*(total_entrees-total_sorties)/12 for i in range(12)] + [solde_fin]
        })

        st.dataframe(df.style.format({
            "Entrées": "{:,.3f} F CFA",
            "Sorties": "{:,.3f} F CFA",
            "Solde cumulée": "{:,.3f} F CFA"
        }))

        # Graphique
        from plotly import express as px
        
        fig = px.line(df, x="Mois", y="Solde cumulée", title=f"Évolution de la trésorerie - {annee}")
        st.plotly_chart(fig)
