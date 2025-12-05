from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
import unidecode


# =============== OUTIL NOM DE GARE ===============


def clean_name(name):
    """Nettoie un nom de gare pour la jointure."""
    if not isinstance(name, str):
        return ""
    name = name.lower().strip()
    name = unidecode.unidecode(name)  # enlève accents
    name = name.replace("(", "").replace(")", "")
    name = name.replace("-", " ")
    name = " ".join(name.split())  # supprime espaces multiples
    return name


# =============== COULEURS UNIFIÉES ===============


MODE_COLOR_MAP = {
    "Métro": "#00F5D4",   # turquoise
    "RER": "#F97316",     # orange néon
    "Train": "#7C3AED",   # violet électrique
    "Tram": "#F472B6",    # rose flashy
    "VAL": "#22C55E",     # vert vif
    "Autre": "#9CA3AF",   # gris
}

NEON_SEQUENCE = [
    "#00F5D4",
    "#F97316",
    "#7C3AED",
    "#F472B6",
    "#22C55E",
    "#38BDF8",
]


# =============== LOCALISATION FICHIERS ===============


BASE_DIR = Path(__file__).resolve().parents[1]


def locate_case_insensitive(name: str) -> Path:
    """Retourne un Path dans BASE_DIR en ignorant la casse."""
    p = BASE_DIR / name
    if p.exists():
        return p
    lname = name.lower()
    for child in BASE_DIR.iterdir():
        if child.name.lower() == lname:
            return child
    return p


VALIDATIONS_PATH = locate_case_insensitive(
    "validations-reseau-ferre-profils-horaires-par-jour-type-1er-trimestre.csv"
)
GARES_PATH = locate_case_insensitive(
    "emplacement-des-gares-idf-data-generalisee.csv"
)


# =============== FONCTIONS DONNÉES TRANSPORT ===============


@st.cache_data
def load_validations_data(path: Path) -> pd.DataFrame:
    """Charge et prépare les données de profils horaires de validations (réseau ferré)."""
    df = pd.read_csv(path, sep=";")

    df = df.rename(
        columns={
            "libelle_arret": "gare",
            "cat_jour": "type_jour",
            "trnc_horr_60": "tranche_horaire",
            "pourcentage_validations": "pct_validations",
        }
    )

    df["pct_validations"] = pd.to_numeric(df["pct_validations"], errors="coerce")

    def parse_heure(tranche):
        if not isinstance(tranche, str):
            return None
        part = tranche.split("-")[0]  # "6H"
        part = part.replace("H", "")
        try:
            return int(part)
        except ValueError:
            return None

    df["heure"] = df["tranche_horaire"].apply(parse_heure)

    df = df.dropna(
        subset=["gare", "type_jour", "tranche_horaire", "pct_validations", "heure"]
    )
    df["heure"] = df["heure"].astype(int)

    df["gare"] = df["gare"].apply(clean_name)

    return df


@st.cache_data
def load_gares_data(path: Path) -> pd.DataFrame:
    """Charge et prépare les données de localisation des gares."""
    df = pd.read_csv(path, sep=";")

    if "nom_long" in df.columns:
        df = df.rename(columns={"nom_long": "gare"})

    if "geo_point_2d" in df.columns:

        def split_geo(s):
            if isinstance(s, str):
                parts = s.split(",")
                if len(parts) == 2:
                    return parts[0].strip(), parts[1].strip()
            return None, None

        df[["lat_str", "lon_str"]] = df["geo_point_2d"].apply(
            lambda x: pd.Series(split_geo(x))
        )
        df["lat"] = pd.to_numeric(df["lat_str"], errors="coerce")
        df["lon"] = pd.to_numeric(df["lon_str"], errors="coerce")

    for col in ["termetro", "terrer", "tertrain", "tertram", "terval"]:
        if col not in df.columns:
            df[col] = 0

    if "mode" not in df.columns:

        def infer_mode(row):
            if row.get("termetro", 0) == 1:
                return "Métro"
            if row.get("terrer", 0) == 1:
                return "RER"
            if row.get("tertrain", 0) == 1:
                return "Train"
            if row.get("tertram", 0) == 1:
                return "Tram"
            if row.get("terval", 0) == 1:
                return "VAL"
            return "Autre"

        df["mode"] = df.apply(infer_mode, axis=1)

    keep_cols = [
        "gare",
        "lat",
        "lon",
        "mode",
        "exploitant",
        "termetro",
        "terrer",
        "tertrain",
        "tertram",
        "terval",
    ]
    keep_cols = [c for c in keep_cols if c in df.columns]
    df = df[keep_cols]

    df = df.dropna(subset=["gare"])
    df["gare"] = df["gare"].apply(clean_name)

    return df


@st.cache_data
def merge_validations_gares(df_val: pd.DataFrame, df_gares: pd.DataFrame) -> pd.DataFrame:
    """Jointure entre profils horaires et géolocalisation des gares."""
    merged = df_val.merge(df_gares, on="gare", how="left")
    return merged


# =============== GRAPHIQUES TRANSPORT ===============


def plot_profil_horaire(df: pd.DataFrame) -> None:
    """Courbe : profil horaire des validations."""
    if df.empty:
        st.info("Aucune donnée pour ce filtre.")
        return

    fig = px.line(
        df.sort_values(["gare", "heure"]),
        x="heure",
        y="pct_validations",
        color="gare",
        markers=True,
        labels={
            "heure": "Heure de la journée",
            "pct_validations": "% des validations journalières",
            "gare": "Gare / station",
        },
        title="Profil horaire des validations par gare",
        template="plotly_dark",
        color_discrete_sequence=NEON_SEQUENCE,
    )
    fig.update_xaxes(dtick=1)
    fig.update_layout(
        plot_bgcolor="#050816",
        paper_bgcolor="#050816",
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_boxplot(df: pd.DataFrame) -> None:
    """Boxplot : distribution des validations par mode de transport."""
    df_plot = df.dropna(subset=["mode"]).copy()
    if df_plot.empty:
        st.info("Aucune donnée avec mode de transport pour ce filtre.")
        return

    fig = px.box(
        df_plot,
        x="mode",
        y="pct_validations",
        color="mode",
        points="all",
        color_discrete_map=MODE_COLOR_MAP,
        labels={
            "mode": "Mode de Transport",
            "pct_validations": "% des validations journalières",
        },
        title="Distribution du % de validations par mode de transport",
        template="plotly_dark",
    )
    order = (
        df_plot.groupby("mode")["pct_validations"]
        .median()
        .sort_values(ascending=False)
        .index
    )
    fig.update_layout(
        xaxis={"categoryorder": "array", "categoryarray": order},
        plot_bgcolor="#050816",
        paper_bgcolor="#050816",
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_heatmap(df: pd.DataFrame) -> None:
    """Heatmap : heure × type de jour."""
    if df.empty:
        return

    pivot = (
        df.groupby(["type_jour", "heure"])["pct_validations"]
        .mean()
        .reset_index()
        .pivot(index="type_jour", columns="heure", values="pct_validations")
    )

    fig = px.imshow(
        pivot,
        aspect="auto",
        labels=dict(x="Heure", y="Type de jour", color="% validations"),
        title="Répartition moyenne des validations par heure et type de jour",
        template="plotly_dark",
        color_continuous_scale="Turbo",
    )
    fig.update_layout(
        plot_bgcolor="#050816",
        paper_bgcolor="#050816",
    )
    st.plotly_chart(fig, use_container_width=True)


def show_map(df_merged: pd.DataFrame) -> None:
    """Carte interactive des gares avec taille proportionnelle aux validations et couleur par mode."""
    df_map = df_merged.dropna(subset=["lat", "lon"]).copy()
    if df_map.empty:
        st.info("Pas de données géolocalisées pour ce filtre.")
        return

    df_map = (
        df_map.groupby(["gare", "lat", "lon", "mode", "exploitant"], as_index=False)[
            "pct_validations"
        ]
        .sum()
        .rename(columns={"pct_validations": "total_pct_validations"})
    )

    fig = px.scatter_mapbox(
        df_map,
        lat="lat",
        lon="lon",
        color="mode",
        size="total_pct_validations",
        hover_name="gare",
        hover_data={
            "mode": True,
            "total_pct_validations": ":.2f",
            "lat": False,
            "lon": False,
        },
        color_discrete_map=MODE_COLOR_MAP,
        zoom=9,
        center={"lat": df_map["lat"].mean(), "lon": df_map["lon"].mean()},
        mapbox_style="carto-positron",
        title="Localisation des gares (Taille = % total de validations)",
    )
    fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
    st.plotly_chart(fig, use_container_width=True)


# =============== PAGE DASHBOARD (LAYOUT NORMAL) ===============


def show_transport_dashboard() -> None:
    st.title("Dashboard Transport — Profils horaires du réseau ferré")
    st.subheader(
        "Analyse des profils horaires de validations et localisation des gares en Île-de-France"
    )

    st.write(
        """
Ce dashboard exploite les **profils horaires de validations** sur le réseau ferré (métro / RER / train)
et les **coordonnées géographiques des gares** pour analyser :

- les **heures de pointe** (courbes et heatmap),
- la **distribution** des validations par **mode de transport** (boxplot),
- la **répartition spatiale** des gares à fort trafic (carte interactive).
        """
    )

    if not VALIDATIONS_PATH.exists() or not GARES_PATH.exists():
        if not VALIDATIONS_PATH.exists():
            st.error(
                "Fichier des profils horaires introuvable. "
                "Place `validations-reseau-ferre-profils-horaires-par-jour-type-1er-trimestre.csv` "
                "à côté de `app.py`."
            )
        if not GARES_PATH.exists():
            st.error(
                "Fichier des gares introuvable. "
                "Place `emplacement-des-gares-idf-data-generalisee.csv` à côté de `app.py`."
            )
        return

    df_val = load_validations_data(VALIDATIONS_PATH)
    df_gares = load_gares_data(GARES_PATH)
    df_merged = merge_validations_gares(df_val, df_gares)

    with st.expander("Aperçu des données et préparation", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Profils horaires (réseau ferré)**")
            st.dataframe(df_val.head(), use_container_width=True)
        with col2:
            st.markdown("**Localisation des gares**")
            st.dataframe(df_gares.head(), use_container_width=True)

    st.markdown("### Filtres")

    type_jour_options = ["Tous"] + sorted(df_val["type_jour"].unique())
    selected_type_jour = st.selectbox("Type de jour", type_jour_options, index=0)

    gares_dispo = sorted(df_merged.dropna(subset=["mode"])["gare"].unique())
    selected_gares = st.multiselect(
        "Gares / stations à afficher",
        gares_dispo,
        default=gares_dispo[:5],
    )

    min_h = int(df_val["heure"].min())
    max_h = int(df_val["heure"].max())
    plage_horaire = st.slider(
        "Plage horaire (heures)",
        min_value=min_h,
        max_value=max_h,
        value=(min_h, max_h),
    )

    df_filtered = df_val.copy()
    if selected_type_jour != "Tous":
        df_filtered = df_filtered[df_filtered["type_jour"] == selected_type_jour]
    if selected_gares:
        df_filtered = df_filtered[df_filtered["gare"].isin(selected_gares)]
    df_filtered = df_filtered[
        (df_filtered["heure"] >= plage_horaire[0])
        & (df_filtered["heure"] <= plage_horaire[1])
    ]

    df_merged_filtered = df_merged.merge(
        df_filtered[["gare", "type_jour", "heure", "pct_validations"]],
        on=["gare", "type_jour", "heure", "pct_validations"],
        how="inner",
    )

    colk1, colk2, colk3 = st.columns(3)
    with colk1:
        st.metric(
            "Gares sélectionnées",
            len(selected_gares) if selected_gares else len(gares_dispo),
        )
    with colk2:
        st.metric("Combinaisons heure × gare", len(df_filtered))
    with colk3:
        st.metric("Types de jour présents", df_filtered["type_jour"].nunique())

    st.divider()

    # 2 graphes côte à côte (50% / 50%)
    col_viz_1, col_viz_2 = st.columns(2)
    with col_viz_1:
        st.markdown("### 1. Profil horaire des validations (Courbes)")
        plot_profil_horaire(df_filtered)
    with col_viz_2:
        st.markdown("### 2. Distribution par mode (Boxplot)")
        plot_boxplot(df_merged_filtered)

    st.divider()

    st.markdown("### 3. Heatmap validations par heure et type de jour")
    if selected_type_jour == "Tous":
        plot_heatmap(df_filtered)
    else:
        st.info(
            "Pour afficher la heatmap complète, sélectionne **Tous** dans le filtre 'Type de jour'."
        )
        plot_heatmap(df_val[df_val["gare"].isin(selected_gares)])

    st.divider()

    st.markdown("### 4. Carte des gares (Réseau ferré - Mapbox)")
    show_map(df_merged_filtered)

    st.divider()

    st.markdown("### Tableau des données filtrées")
    st.dataframe(
        df_filtered.sort_values(["gare", "heure"]),
        use_container_width=True,
    )

    st.markdown("### Synthèse des enseignements")
    st.write(
        """
- Le **profil horaire** met en évidence les **heures de pointe** (pics du % de validations).  
- Le **Boxplot** permet de comparer la **dispersion** et les **pics de trafic** selon le **mode de transport** (Métro, RER, etc.).  
- La **heatmap** permet de comparer les dynamiques selon les **types de jour** (semaine, week-end, etc.).  
- La **carte des gares** offre une vision géographique du trafic, avec des points **colorés par mode** et **dimensionnés par le total des validations**.
        """
    )


def main():
    show_transport_dashboard()


if __name__ == "__main__":
    main()
