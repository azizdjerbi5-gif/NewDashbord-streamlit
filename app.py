import streamlit as st

st.set_page_config(
    page_title="Portfolio & Dashboard Transport — Aziz Djerbi",
    page_icon="👨‍💻",
    layout="wide",
)

# Carte d’intro avec bordure
with st.container(border=True):
    title_col, badge_col = st.columns([4, 1])

    with title_col:
        st.markdown("### 👨‍💻 Portfolio & Dashboard Transport")
        st.title("Aziz DJERBI")

    with badge_col:
        st.markdown(
            "<div style='text-align:right; font-size:0.9rem;'>"
            "<span style='padding:4px 8px; border-radius:999px; "
            "background-color:#22c55e; color:#020617; font-weight:600;'>Alternance Data / BI 2025</span>"
            "</div>",
            unsafe_allow_html=True,
        )

    st.write(
        """
Bienvenue sur mon application **Streamlit multipage**, réalisée dans le cadre de ma formation en Science des Données.  
Elle rassemble un **dashboard d’analyse de données de transport** et un **CV interactif** pour mettre en avant mon profil Data / BI.
"""
    )

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 🎯 Objectifs de l’application")
        st.write(
            """
- Manipuler des **données réelles** de validations sur le réseau ferré francilien.  
- Construire des **visualisations interactives** pour comprendre les comportements de mobilité.  
- Montrer une approche **proche du terrain** : indicateurs clairs, mise en forme soignée, et navigation simple.
"""
        )

    with col_right:
        st.markdown("#### 🛠️ Pile technologique")
        st.write(
            """
- **Python** pour le traitement de données.  
- **Pandas** pour le nettoyage et la préparation des jeux de données.  
- **Plotly** pour les graphiques interactifs.  
- **Streamlit** pour la partie web et l’architecture multipage.
"""
        )

st.divider()

# Bloc explicatif sur les pages
with st.container(border=True):
    st.markdown("#### 📂 Contenu des pages")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("**Dashboard transport**")
        st.write(
            """
Page dédiée à l’**analyse des profils horaires de validations** sur le réseau ferré (métro, RER, train, tram, VAL).  
On peut y :
- filtrer par **type de jour** et par **gare** ;
- observer les **heures de pointe** via les courbes et la heatmap ;
- visualiser la **répartition spatiale** du trafic grâce à une carte interactive des gares.
"""
        )

    with col2:
        st.markdown("**CV Portfolio**")
        st.write(
            """
Page orientée **présentation de mon profil** : formation, expériences, projets académiques et compétences techniques.  
Le CV est interactif :
- navigation par **onglets** (profil, expériences, projets, compétences, etc.) ;  
- visualisation du **niveau de maîtrise** des outils via des barres de progression ;  
- possibilité de **télécharger mon CV** au format PDF.
"""
        )

st.divider()

st.markdown(
    """
💡 N’hésite pas à commencer par le **Dashboard transport** pour voir la partie Data en action,
puis à explorer le **CV Portfolio** pour découvrir davantage mon parcours.
"""
)
