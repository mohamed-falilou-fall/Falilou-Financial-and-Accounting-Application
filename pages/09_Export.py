import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

def run():
    st.title("Export & restitution professionnelle")

    st.markdown("### Synthèse financière")

    # Données
    df_synthese = pd.DataFrame({
        "Indicateur": ["Chiffre d'affaires", "Charges totales", "Résultat net", "CAF"],
        "Valeur": [500000, 350000, 150000, 170000]
    })

    st.dataframe(df_synthese.style.format({"Valeur": "{:,.0f}"}))

    # Graphique de synthèse
    fig = px.bar(df_synthese, x="Indicateur", y="Valeur", title="Synthèse financière – vue investisseur")
    st.plotly_chart(fig, use_container_width=True)

    # Export Excel
    st.markdown("### Export Excel")
    def export_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Synthèse")
        return output.getvalue()

    excel_data = export_excel(df_synthese)

    st.download_button(label="Télécharger le rapport Excel",
                       data=excel_data,
                       file_name="Synthese_Financiere.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Export PDF (structure)
    st.markdown("### Export PDF")
    st.info("Le PDF peut être généré à partir de cette synthèse via ReportLab ou WeasyPrint (HTML → PDF). Structure prête pour impression professionnelle.")
    st.success("Module d’export prêt pour restitution investisseurs / banques")
