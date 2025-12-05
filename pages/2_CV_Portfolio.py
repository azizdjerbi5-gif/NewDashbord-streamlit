from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[1]
PHOTO_PATH = BASE_DIR / "photo.jpg"
PDF_PATH = BASE_DIR / "CV_Aziz_Djerbi.pdf"

NEON_SEQUENCE = [
    "#00F5D4",
    "#F97316",
    "#7C3AED",
    "#F472B6",
    "#22C55E",
    "#38BDF8",
]


def show_cv() -> None:
    # En-tête type "carte" CV
    with st.container(border=True):
        left, right = st.columns([1, 3], vertical_alignment="center")

        with left:
            if PHOTO_PATH.exists():
                st.image(
                    PHOTO_PATH,
                    caption="Aziz DJERBI",
                    use_container_width=True,
                )
            else:
                st.warning(
                    "Photo introuvable. Place **photo.jpg** (ou .jpeg/.png) à côté de `app.py`."
                )

        with right:
            st.markdown("#### Data / BI — Alternance 2025")
            st.title("Aziz DJERBI")
            st.write("📍 Pierrefitte-sur-Seine • 🚗 Permis B • 📞 07 78 16 05 47")
            st.write("En recherche d’un **contrat d’alternance** dans la Data.")

            col_btn1, col_btn2 = st.columns([1, 2])
            with col_btn1:
                if PDF_PATH.exists():
                    st.download_button(
                        "📄 Télécharger le CV",
                        PDF_PATH.read_bytes(),
                        file_name=PDF_PATH.name,
                        mime="application/pdf",
                        use_container_width=True,
                        type="primary",
                    )
                else:
                    st.info(
                        "Place **CV_Aziz_Djerbi.pdf** à côté de `app.py` pour activer le téléchargement."
                    )
            with col_btn2:
                st.caption(
                    "SQL • Python • Power BI • Excel • Dash/Plotly • Cloud (AWS, OVH, Azure)"
                )

    st.divider()

    tab_profil, tab_exp, tab_form, tab_proj, tab_comp, tab_lang = st.tabs(
        [
            "Profil",
            "Expériences",
            "Formations",
            "Projets",
            "Compétences",
            "Langues & Intérêts",
        ]
    )

    # Profil
    with tab_profil:
        st.subheader("Profil")
        st.write(
            "Passionné par l’analyse de données et la programmation, orienté business et automatisation. "
            "Intéressé par les problématiques de **coûts**, **performance** et **qualité de données**."
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Domaines clés", "Data / BI")
            st.caption("SQL • Python • Power BI • Excel")
        with c2:
            st.metric("Dev & Outils", "Tech polyvalente")
            st.caption("Dash/Plotly • HTML/CSS • VBA • Access • SAS • R")
        with c3:
            st.metric("Soft skills", "Autonomie")
            st.caption("Esprit d’analyse • Pédagogie • Travail en équipe")

    # Expériences
    with tab_exp:
        st.subheader("Expériences professionnelles")
        with st.container(border=True):
            st.markdown(
                "**Stagiaire Data Analyst — Laevitas (Tunis)**  \n"
                "*Fin juin – Août 2025 (2 mois et 9 jours)*"
            )
            st.markdown(
                "- Monitoring des **coûts cloud** *(AWS, OVH, Azure)* avec un pipeline data (collecte → nettoyage → stockage SQLite → dashboards).  \n"
                "- Mise en place de **KPI** et de **dashboards interactifs** *(Dash/Plotly)* pour suivre les dépenses et alerter sur les dérives."
            )

    # Formations
    with tab_form:
        st.subheader("Formations")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            with st.container(border=True):
                st.markdown(
                    "**BUT Science des Données (2e année)**  \n"
                    "IUT de Paris – Rives de Seine *(2023–2026)*"
                )
        with col_f2:
            with st.container(border=True):
                st.markdown(
                    "**Baccalauréat Général**  \n"
                    "Lycée La Salle – Saint-Rosaire *(2020–2023)*"
                )

    # Projets
    with tab_proj:
        st.subheader("Projets académiques")
        c1, c2 = st.columns(2)

        with c1:
            with st.container(border=True):
                st.markdown("**Enquête IA** *(Nov. 2023 – Janv. 2024)*")
                st.caption(
                    "Analyse d’un questionnaire sur l’IA avec Excel, visualisation et restitution orale."
                )
            with st.container(border=True):
                st.markdown("**Étude de cas** *(Oct. 2023 – Nov. 2023)*")
                st.caption(
                    "Traitement de données avec Excel / Word, graphiques et synthèse pour répondre à une problématique."
                )

        with c2:
            with st.container(border=True):
                st.markdown("**Reporting ventes DVD** *(Janv. 2024)*")
                st.caption(
                    "Extraction SQL, indicateurs clés et recommandations business dans Excel."
                )
            with st.container(border=True):
                st.markdown("**Nettoyage de fichiers de données** *(Déc. 2023)*")
                st.caption(
                    "Scripts Python pour nettoyer, fusionner et convertir des fichiers hétérogènes en CSV propres."
                )

    # Compétences
    with tab_comp:
        st.subheader("Compétences — niveaux (0–100)")

        core = pd.DataFrame(
            {
                "Compétence": ["SQL", "Python", "Excel", "Power BI", "R"],
                "Niveau": [80, 75, 85, 70, 60],
            }
        )
        tools = pd.DataFrame(
            {
                "Compétence": ["HTML/CSS", "VBA", "Access", "SAS"],
                "Niveau": [65, 70, 60, 50],
            }
        )

        colA, colB = st.columns(2)
        with colA:
            st.markdown("**Data / BI**")
            st.dataframe(
                core,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Compétence": st.column_config.TextColumn("Compétence"),
                    "Niveau": st.column_config.ProgressColumn(
                        "Niveau",
                        help="Auto-évaluation",
                        min_value=0,
                        max_value=100,
                        format="%d%%",
                    ),
                },
            )
        with colB:
            st.markdown("**Dev / Outils**")
            st.dataframe(
                tools,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Compétence": st.column_config.TextColumn("Compétence"),
                    "Niveau": st.column_config.ProgressColumn(
                        "Niveau",
                        help="Auto-évaluation",
                        min_value=0,
                        max_value=100,
                        format="%d%%",
                    ),
                },
            )

        st.markdown("#### Vue synthétique des compétences principales")
        core_plot = core.set_index("Compétence")
        fig_comp = px.bar(
            core_plot,
            x=core_plot.index,
            y="Niveau",
            color=core_plot.index,
            range_y=[0, 100],
            color_discrete_sequence=NEON_SEQUENCE,
            labels={"Niveau": "Niveau (0–100)", "Compétence": "Compétence"},
            title="Niveau par compétence Data / BI",
        )
        fig_comp.update_layout(
            showlegend=False,
            template="plotly_dark",
            plot_bgcolor="#050816",
            paper_bgcolor="#050816",
        )
        st.plotly_chart(fig_comp, use_container_width=True)

        st.caption(
            "Les niveaux sont une auto‑évaluation, modifiables facilement dans les tableaux ci‑dessus."
        )

    # Langues & intérêts
    with tab_lang:
        st.subheader("Langues & Intérêts")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Langues**")
            st.write("- Anglais **B2**")
            st.write("- Allemand **B1**")
        with c2:
            st.markdown("**Centres d’intérêt**")
            st.write("- Football")
            st.write("- Jeux vidéo")
            st.write("- Automobile")

    st.divider()
    st.caption("© Aziz DJERBI — CV interactif Streamlit")


def main():
    show_cv()


if __name__ == "__main__":
    main()
