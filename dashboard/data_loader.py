from pathlib import Path

import pandas as pd
import streamlit as st

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "clean"
    / "bq-results-last-12-months-clean.csv"
)


@st.cache_data
def load_dashboard_data():
    """Charge et normalise le jeu de données GDELT clean pour le dashboard."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Fichier de données introuvable: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE, low_memory=False)

    quadclass_map = {
        1: "Coopération Verbale",
        2: "Coopération Matérielle",
        3: "Conflit Verbal",
        4: "Conflit Matériel",
    }

    df["date"] = pd.to_datetime(df["SQLDATE"], errors="coerce")
    df["event_type"] = pd.to_numeric(df["QuadClass"], errors="coerce").map(
        quadclass_map
    )

    geo_parts = (
        df["ActionGeo_FullName"].fillna("").astype(str).str.split(",", n=2, expand=True)
    )
    df["ville"] = geo_parts[0].fillna("").str.strip().str.strip('"')
    df["departement"] = geo_parts[1].fillna("").str.strip().str.strip('"')
    df["goldstein"] = pd.to_numeric(df["GoldsteinScale"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["ActionGeo_Lat"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["ActionGeo_Long"], errors="coerce")
    df["fatalities"] = 0

    df = df[
        df["date"].notna()
        & df["event_type"].notna()
        & df["goldstein"].notna()
        & df["latitude"].notna()
        & df["longitude"].notna()
        & df["departement"].ne("")
        & df["departement"].str.lower().ne("benin")
        & df["departement"].str.lower().ne("unknown")
        & df["ville"].ne("")
        & df["ville"].str.lower().ne("benin")
        & df["ville"].str.lower().ne("unknown")
    ].copy()

    df["semaine"] = df["date"].dt.isocalendar().week.astype(int)

    return df[
        [
            "date",
            "departement",
            "ville",
            "event_type",
            "goldstein",
            "latitude",
            "longitude",
            "fatalities",
            "semaine",
        ]
    ].copy()
