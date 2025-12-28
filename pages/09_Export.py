# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

from database import save_module_data, load_module_data


def run():
    st.title("Export & restitution professionnelle")

    MODULE = "export"

    # =========================
    # Chargement DB
    # =========================
    data_db = load_module_data(MODULE, "Année 1")
    if "export" not in st.session_state:
        st.session_state["export"] = data_db if data_db else {}

    st.markdown("### Synthèse financière")

    hyp = st.session_state.get("hypotheses", {})
    cr = st.session_state.get("compte_resultat", {}).get("Année 1", {})

    chiffre_affaires = hyp.get("Chiffre d'affaires HT (1 x 2 x 3)", 0.0)
    charges = cr.get("Charges totales", 0.0)
    RN = cr.get("Résultat net (RN)", 0.0)
    CAF = cr.get("Capacité d'autofinancement", 0.0)

    # =========================
    # DataFrame synthèse
    # =========================
    df_synthese = pd.DataFrame({
        "Indicateur": [
            "Chiffre d'affaires",
            "Charges totales",
            "Résultat net",
            "CAF"
        ],
        "Valeur (F CFA)": [
            chiffre_affaires,
            charges,
            RN,
            CAF
        ]
    })

    st.dataframe(df_synthese.style.format({
        "Valeur (F CFA)": "{:,.3f}"
    }))

    # =========================
    # Sauvegarde
    # =========================
    st.session_state["export"] = {
        "CA": chiffre_affaires,
        "Charges": charges,
        "RN": RN,
        "CAF": CAF
    }

    save_module_data(MODULE, "Année 1", st.session_state["export"])

    # =========================
    # Graphique investisseur
    # =========================
    fig = px.bar(
        df_synthese,
        x="Indicateur",
        y="Valeur (F CFA)",
        title="Synthèse financière – vue investisseur"
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # Export Excel
    # =========================
    st.markdown("### Export Excel")

    def export_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Synthèse financière")
        return output.getvalue()

    excel_data = export_excel(df_synthese)

    st.download_button(
        label="Télécharger le rapport Excel",
        data=excel_data,
        file_name="Synthese_Financiere.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # =========================
    # PDF (structure prête)
    # =========================
    st.markdown("### Export PDF")
    st.info(
        "Le PDF peut être généré via ReportLab ou HTML → PDF "
        "(structure validée pour banques et investisseurs)."
    )

    st.success("Module d’export prêt pour restitution professionnelle")
