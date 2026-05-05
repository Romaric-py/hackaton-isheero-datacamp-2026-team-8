"""
=============================================================
  HACKATHON 2026 — Bénin Insights Challenge
  TABLEAU DE BORD TACTIQUE - ANALYSE DES INSIGHTS AU Bénin À PARTIR DES DONNÉES GDELT (12 DERNIERS MOIS)
  Focus : Stabilité, Conflits, Réactivité de l'État, Zones à Risque
=============================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────
# CONFIG GLOBALE
# ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Tableau de Bord Tactique – Bénin",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────
# THÈME CSS SOMBRE PERSONNALISÉ
# ─────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ─────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=IBM+Plex+Mono:wght@400;600&family=Barlow:ital,wght@0,300;0,400;0,600;1,300&display=swap');

html, body, [class*="css"] {
    background-color: #0D0F1A !important;
    color: #E0E4F0 !important;
    font-family: 'Barlow', sans-serif;
}

/* ── Sidebar ──────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A0C17 0%, #111425 100%) !important;
    border-right: 1px solid #1E2240;
}
section[data-testid="stSidebar"] * { color: #C8CDE8 !important; }

/* ── Titres ───────────────────────────────────── */
h1, h2, h3 { font-family: 'Rajdhani', sans-serif !important; letter-spacing: 1px; }
h1 { font-size: 2.2rem !important; color: #FF4E5B !important; text-transform: uppercase; }
h2 { color: #6C8EFF !important; font-size: 1.4rem !important; border-bottom: 1px solid #1E2240; padding-bottom: 6px; }
h3 { color: #A0A8D0 !important; font-size: 1.1rem !important; }

/* ── KPI Cards ────────────────────────────────── */
.kpi-card {
    background: linear-gradient(135deg, #131628 0%, #1A1E35 100%);
    border: 1px solid #252A48;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); }
.kpi-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: var(--accent);
}
.kpi-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2.4rem;
    font-weight: 600;
    color: var(--accent);
    line-height: 1.1;
}
.kpi-label {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #7080A0;
    margin-top: 6px;
}
.kpi-delta {
    font-size: 0.82rem;
    color: #60D080;
    margin-top: 4px;
}

/* ── Section header ───────────────────────────── */
.section-header {
    display: flex; align-items: center; gap: 10px;
    margin: 32px 0 16px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.2rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 2px;
    color: #8090C0;
}
.section-header span { font-size: 1.4rem; }

/* ── Alert boxes ──────────────────────────────── */
div[data-testid="stAlert"] {
    border-radius: 8px !important;
    border-left: 4px solid !important;
    background: #131628 !important;
}

/* ── Divider ──────────────────────────────────── */
hr { border-color: #1E2240 !important; margin: 28px 0 !important; }

/* ── Plotly bg override ───────────────────────── */
.js-plotly-plot .plotly { background: transparent !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────
# GÉNÉRATION DES DONNÉES SIMULÉES
# ─────────────────────────────────────────────────
@st.cache_data
def generate_data():
    """Génère un jeu de données ACLED-like pour le Bénin 2025."""
    np.random.seed(42)

    departements = {
        "Alibori":      {"lat": 11.45, "lon": 2.85,  "weight": 0.18},
        "Atacora":      {"lat": 10.55, "lon": 1.35,  "weight": 0.14},
        "Atlantique":   {"lat": 6.55,  "lon": 2.15,  "weight": 0.12},
        "Borgou":       {"lat": 9.75,  "lon": 2.70,  "weight": 0.16},
        "Collines":     {"lat": 8.20,  "lon": 2.25,  "weight": 0.09},
        "Couffo":       {"lat": 7.00,  "lon": 1.85,  "weight": 0.07},
        "Donga":        {"lat": 9.75,  "lon": 1.65,  "weight": 0.08},
        "Littoral":     {"lat": 6.37,  "lon": 2.42,  "weight": 0.06},
        "Mono":         {"lat": 6.80,  "lon": 1.60,  "weight": 0.05},
        "Ouémé":        {"lat": 6.60,  "lon": 2.55,  "weight": 0.06},
        "Plateau":      {"lat": 7.15,  "lon": 2.60,  "weight": 0.05},
        "Zou":          {"lat": 7.30,  "lon": 2.10,  "weight": 0.07},
    }

    villes = {
        "Alibori":    ["Kandi", "Malanville", "Gogounou", "Banikoara"],
        "Atacora":    ["Natitingou", "Tanguieta", "Boukoumbé", "Cobly"],
        "Atlantique": ["Abomey-Calavi", "Allada", "Ouidah", "Toffo"],
        "Borgou":     ["Parakou", "Tchaourou", "N'Dali", "Pèrèrè"],
        "Collines":   ["Dassa-Zoumé", "Savalou", "Savè", "Glazoué"],
        "Couffo":     ["Aplahoué", "Djakotomey", "Klouékanmè", "Toviklin"],
        "Donga":      ["Djougou", "Bassila", "Copargo", "Ouaké"],
        "Littoral":   ["Cotonou", "Akpakpa", "Cadjèhoun", "Godomey"],
        "Mono":       ["Lokossa", "Comè", "Athiémé", "Grand-Popo"],
        "Ouémé":      ["Porto-Novo", "Sèmè-Kpodji", "Adjarra", "Akpro-Missérété"],
        "Plateau":    ["Pobè", "Kétou", "Adja-Ouèrè", "Ifangni"],
        "Zou":        ["Abomey", "Bohicon", "Covè", "Agbangnizoun"],
    }

    event_types = {
        "Conflit Matériel":      {"color": "#FF3A4A", "goldstein_range": (-10, -3)},
        "Conflit Verbal":        {"color": "#FF9500", "goldstein_range": (-3,  0)},
        "Coopération Matérielle":{"color": "#3A7EFF", "goldstein_range": (1,   7)},
        "Coopération Verbale":   {"color": "#30C080", "goldstein_range": (0,   3)},
    }

    dept_list = list(departements.keys())
    dept_weights = [departements[d]["weight"] for d in dept_list]

    # Dates : Jan 2025 → Dec 2025
    start = datetime(2025, 1, 1)
    end   = datetime(2025, 12, 31)

    n = 1800
    records = []
    for _ in range(n):
        dept = np.random.choice(dept_list, p=dept_weights / np.array(dept_weights).sum())
        ville = np.random.choice(villes[dept])

        # Pic en décembre pour la zone nord (Alibori/Borgou)
        if dept in ["Alibori", "Borgou", "Atacora"]:
            # Probabilité augmentée en Q4
            day_idx = int(np.random.beta(1.8, 1.2) * (end - start).days)
        else:
            day_idx = int(np.random.uniform(0, (end - start).days))

        date = start + timedelta(days=day_idx)

        # Type d'événement pondéré par département
        if dept in ["Alibori", "Borgou", "Atacora", "Donga"]:
            et_weights = [0.40, 0.28, 0.18, 0.14]
        elif dept in ["Littoral", "Atlantique", "Ouémé"]:
            et_weights = [0.15, 0.20, 0.40, 0.25]
        else:
            et_weights = [0.22, 0.25, 0.32, 0.21]

        et_labels = list(event_types.keys())
        evt = np.random.choice(et_labels, p=et_weights)

        gs_min, gs_max = event_types[evt]["goldstein_range"]
        goldstein = round(np.random.uniform(gs_min, gs_max), 2)

        # Coordonnées légèrement dispersées
        lat = departements[dept]["lat"] + np.random.uniform(-0.6, 0.6)
        lon = departements[dept]["lon"] + np.random.uniform(-0.6, 0.6)

        records.append({
            "date":        date,
            "annee":       date.year,
            "mois":        date.month,
            "mois_label":  date.strftime("%b %Y"),
            "departement": dept,
            "ville":       ville,
            "event_type":  evt,
            "goldstein":   goldstein,
            "latitude":    lat,
            "longitude":   lon,
            "fatalities":  max(0, int(np.random.exponential(0.3)) if evt == "Conflit Matériel" else 0),
        })

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    df["semaine"] = df["date"].dt.isocalendar().week.astype(int)
    return df


# ─────────────────────────────────────────────────
# COULEURS & CONSTANTES
# ─────────────────────────────────────────────────
COLOR_MAP = {
    "Conflit Matériel":       "#FF3A4A",
    "Conflit Verbal":         "#FF9500",
    "Coopération Matérielle": "#3A7EFF",
    "Coopération Verbale":    "#30C080",
}

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(13,15,26,0.6)",
    font=dict(color="#C0C8E0", family="Barlow, sans-serif"),
    xaxis=dict(gridcolor="#1E2240", linecolor="#2A3060", zeroline=False),
    yaxis=dict(gridcolor="#1E2240", linecolor="#2A3060", zeroline=False),
    legend=dict(bgcolor="rgba(13,15,26,0.7)", bordercolor="#252A48", borderwidth=1),
    margin=dict(l=20, r=20, t=50, b=20),
)


# ─────────────────────────────────────────────────
# CHARGEMENT DES DONNÉES
# ─────────────────────────────────────────────────
df_raw = generate_data()

# ─────────────────────────────────────────────────
# SIDEBAR – FILTRES
# ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 12px 0 24px;'>
        <div style='font-family:Rajdhani;font-size:1.5rem;font-weight:700;
                    color:#FF4E5B;text-transform:uppercase;letter-spacing:3px;'>
            🛡️ TABLEAU<br>TACTIQUE
        </div>
        <div style='font-size:0.7rem;color:#5060A0;letter-spacing:2px;margin-top:4px;'>
            ANALYSE DE CRISE · BÉNIN 2025
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📅 Période d'analyse")
    date_min = df_raw["date"].min().date()
    date_max = df_raw["date"].max().date()

    all_months = sorted(df_raw["date"].dt.to_period("M").unique())
    month_labels = [str(m) for m in all_months]

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        start_idx = st.selectbox("De", options=range(len(month_labels)),
                                 format_func=lambda i: month_labels[i], index=0)
    with col_s2:
        end_idx = st.selectbox("À", options=range(len(month_labels)),
                               format_func=lambda i: month_labels[i], index=len(month_labels)-1)

    if start_idx > end_idx:
        st.warning("⚠️ Date de début > date de fin.")
        start_idx, end_idx = end_idx, start_idx

    selected_start = pd.Period(month_labels[start_idx], freq="M").start_time
    selected_end   = pd.Period(month_labels[end_idx],   freq="M").end_time

    st.markdown("---")
    st.markdown("### 🗺️ Départements")
    all_depts = sorted(df_raw["departement"].unique())
    selected_depts = st.multiselect(
        "Sélectionner",
        options=all_depts,
        default=all_depts,
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### 🎯 Types d'événements")
    all_types = list(COLOR_MAP.keys())
    selected_types = st.multiselect(
        "Types",
        options=all_types,
        default=all_types,
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.caption("💡 Tous les graphiques se mettent à jour en temps réel selon vos filtres.")


# ─────────────────────────────────────────────────
# FILTRAGE
# ─────────────────────────────────────────────────
if not selected_depts:
    selected_depts = all_depts
if not selected_types:
    selected_types = all_types

df = df_raw[
    (df_raw["date"] >= selected_start) &
    (df_raw["date"] <= selected_end) &
    (df_raw["departement"].isin(selected_depts)) &
    (df_raw["event_type"].isin(selected_types))
].copy()


# ─────────────────────────────────────────────────
# EN-TÊTE
# ─────────────────────────────────────────────────
st.markdown("""
<h1 style='margin-bottom:0;'>🛡️ TABLEAU DE BORD TACTIQUE</h1>
<p style='color:#5A6A90;font-family:IBM Plex Mono,monospace;font-size:0.8rem;margin-top:4px;'>
    ANALYSE DE SÉCURITÉ ET DE STABILITÉ — BÉNIN 2025 &nbsp;|&nbsp; Hackathon Edition
</p>
<hr>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────
# SECTION 1 – KPIs
# ─────────────────────────────────────────────────
st.markdown("## 📊 Chiffres Clés")

if df.empty:
    st.error("Aucune donnée pour les filtres sélectionnés.")
    st.stop()

total_incidents   = len(df)
goldstein_moy     = df["goldstein"].mean()
dept_le_plus_touche = df[df["event_type"].str.contains("Conflit")]["departement"].value_counts().idxmax() if not df[df["event_type"].str.contains("Conflit")].empty else "N/A"
nb_conflits       = df[df["event_type"].str.contains("Conflit")].shape[0]
nb_coops          = df[df["event_type"].str.contains("Coopération")].shape[0]
ratio_reactivite  = nb_coops / nb_conflits if nb_conflits > 0 else 0
total_fatalities  = df["fatalities"].sum()

col1, col2, col3, col4, col5 = st.columns(5)

kpis = [
    (col1, total_incidents, "Incidents Totaux", "#FF4E5B", f"📍 {len(selected_depts)} depts"),
    (col2, f"{goldstein_moy:.2f}", "Score de Stabilité", "#6C8EFF" if goldstein_moy >= 0 else "#FF4E5B", "Indice Goldstein moyen"),
    (col3, dept_le_plus_touche, "Dept. le + Touché", "#FF9500", "Zone de conflit prioritaire"),
    (col4, f"{ratio_reactivite:.2f}", "Ratio Réactivité", "#30C080", "Actions/Réactions État"),
    (col5, int(total_fatalities), "Victimes Signalées", "#FF3A4A", "Total décès rapportés"),
]

for col, val, label, accent, delta in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card" style="--accent:{accent};">
            <div class="kpi-value">{val}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-delta">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Alertes dynamiques ─────────────────────────
alert_col1, alert_col2, alert_col3 = st.columns(3)

with alert_col1:
    if ratio_reactivite < 0.05:
        st.error("⚠️ **Alerte Critique** : Capacité de réponse de l'État quasi-nulle sur cette période. Ratio réactivité < 0.05")
    elif ratio_reactivite < 0.3:
        st.warning(f"⚡ **Réactivité Faible** : Le ratio Action/Réaction est de **{ratio_reactivite:.2f}**. La réponse institutionnelle reste insuffisante.")
    else:
        st.success(f"✅ **Réactivité Satisfaisante** : Ratio de **{ratio_reactivite:.2f}** — La réponse de l'État suit l'évolution des conflits.")

with alert_col2:
    pct_conflit = nb_conflits / total_incidents * 100 if total_incidents > 0 else 0
    if pct_conflit > 60:
        st.error(f"🔴 **Zone Rouge** : {pct_conflit:.0f}% des événements sont des conflits. Situation alarmante.")
    elif pct_conflit > 40:
        st.warning(f"🟡 **Zone de Tension** : {pct_conflit:.0f}% des événements sont conflictuels. Surveillance accrue recommandée.")
    else:
        st.info(f"🔵 **Zone Modérée** : {pct_conflit:.0f}% de conflits. Dynamique globalement stable.")

with alert_col3:
    if goldstein_moy < -3:
        st.error(f"📉 **Stabilité Critique** : Score Goldstein de **{goldstein_moy:.2f}**. Risque de déstabilisation élevé.")
    elif goldstein_moy < 0:
        st.warning(f"⚠️ **Instabilité Latente** : Score Goldstein de **{goldstein_moy:.2f}**. Tendance négative à surveiller.")
    else:
        st.success(f"📈 **Stabilité Positive** : Score Goldstein de **{goldstein_moy:.2f}**. Dynamique coopérative dominante.")

st.markdown("---")


# ─────────────────────────────────────────────────
# SECTION 2 – PANORAMA DE LA CRISE (Stacked Bar)
# ─────────────────────────────────────────────────
st.markdown("## 🏛️ Panorama de la Crise par Département")

dept_type = (
    df.groupby(["departement", "event_type"])
    .size()
    .reset_index(name="count")
)
dept_order = (
    dept_type[dept_type["event_type"].str.contains("Conflit")]
    .groupby("departement")["count"].sum()
    .sort_values(ascending=False)
    .index.tolist()
)

fig_bar = go.Figure()
for evt_type, color in COLOR_MAP.items():
    if evt_type not in selected_types:
        continue
    data_t = dept_type[dept_type["event_type"] == evt_type]
    dept_counts = {r["departement"]: r["count"] for _, r in data_t.iterrows()}
    fig_bar.add_trace(go.Bar(
        name=evt_type,
        x=dept_order,
        y=[dept_counts.get(d, 0) for d in dept_order],
        marker_color=color,
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>" + evt_type + ": <b>%{y}</b><extra></extra>",
    ))

fig_bar.update_layout(
    barmode="stack",
    title=dict(text="Répartition des événements par département", font=dict(size=14, color="#8090C0")),
    height=400,
    **PLOTLY_THEME,
    xaxis=dict(**PLOTLY_THEME["xaxis"], tickangle=-30),
)
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")


# ─────────────────────────────────────────────────
# SECTION 3 – DYNAMIQUE TEMPORELLE
# ─────────────────────────────────────────────────
st.markdown("## 📈 Dynamique Temporelle des Incidents")

tab1, tab2 = st.tabs(["📅 Évolution mensuelle (Line Chart)", "📊 Évolution hebdomadaire"])

with tab1:
    df["mois_period"] = df["date"].dt.to_period("M").dt.to_timestamp()
    monthly = (
        df.groupby(["mois_period", "event_type"])
        .size()
        .reset_index(name="count")
    )

    fig_line = go.Figure()
    for evt_type, color in COLOR_MAP.items():
        if evt_type not in selected_types:
            continue
        sub = monthly[monthly["event_type"] == evt_type].sort_values("mois_period")
        fig_line.add_trace(go.Scatter(
            x=sub["mois_period"],
            y=sub["count"],
            name=evt_type,
            mode="lines+markers",
            line=dict(color=color, width=2.5),
            marker=dict(size=6, color=color, line=dict(color="#0D0F1A", width=1.5)),
            hovertemplate="<b>%{x|%b %Y}</b><br>" + evt_type + ": <b>%{y}</b><extra></extra>",
            fill="tozeroy",
            fillcolor=color.replace(")", ",0.07)").replace("rgb", "rgba").replace("#", "rgba(") if color.startswith("#") else color,
        ))

    # Zone de pic décembre
    fig_line.add_vrect(
        x0="2025-11-01", x1="2025-12-31",
        fillcolor="rgba(255,60,74,0.06)",
        line_width=0,
        annotation_text="📍 Pic Q4",
        annotation_position="top left",
        annotation_font=dict(color="#FF4E5B", size=11),
    )

    fig_line.update_layout(
        title=dict(text="Évolution mensuelle des 4 grands types d'événements", font=dict(size=14, color="#8090C0")),
        height=420,
        **PLOTLY_THEME,
        xaxis=dict(**PLOTLY_THEME["xaxis"], dtick="M1", tickformat="%b %Y"),
        hovermode="x unified",
    )
    st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    weekly = (
        df.groupby(["semaine", "event_type"])
        .size()
        .reset_index(name="count")
    )
    fig_wk = go.Figure()
    for evt_type, color in COLOR_MAP.items():
        if evt_type not in selected_types:
            continue
        sub = weekly[weekly["event_type"] == evt_type].sort_values("semaine")
        fig_wk.add_trace(go.Bar(
            x=sub["semaine"], y=sub["count"],
            name=evt_type, marker_color=color, marker_line_width=0,
            hovertemplate="Semaine %{x}<br>" + evt_type + ": <b>%{y}</b><extra></extra>",
        ))
    fig_wk.update_layout(
        barmode="stack",
        title=dict(text="Activité hebdomadaire (par numéro de semaine ISO)", font=dict(size=14, color="#8090C0")),
        height=380, **PLOTLY_THEME,
        xaxis=dict(**PLOTLY_THEME["xaxis"], title="Semaine de l'année"),
    )
    st.plotly_chart(fig_wk, use_container_width=True)

st.markdown("---")


# ─────────────────────────────────────────────────
# SECTION 4 – CARTOGRAPHIE TACTIQUE (Bubble Map)
# ─────────────────────────────────────────────────
st.markdown("## 🗺️ Cartographie Tactique — Points Chauds")

map_agg = (
    df.groupby(["ville", "departement", "event_type", "latitude", "longitude"])
    .agg(count=("goldstein", "count"), goldstein_moy=("goldstein", "mean"), fatalities=("fatalities", "sum"))
    .reset_index()
)

# Agréger par ville tous types confondus pour la taille des bulles
ville_agg = (
    df.groupby(["ville", "departement", "latitude", "longitude"])
    .agg(total=("goldstein", "count"), goldstein_moy=("goldstein", "mean"), fatalities=("fatalities", "sum"))
    .reset_index()
)
ville_agg["type_dominant"] = (
    df.groupby("ville")["event_type"]
    .agg(lambda x: x.value_counts().index[0])
    .reindex(ville_agg["ville"])
    .values
)
ville_agg["color"] = ville_agg["type_dominant"].map(COLOR_MAP)
ville_agg["hover"] = (
    "<b>" + ville_agg["ville"] + "</b> (" + ville_agg["departement"] + ")<br>"
    + "Incidents: <b>" + ville_agg["total"].astype(str) + "</b><br>"
    + "Goldstein moyen: <b>" + ville_agg["goldstein_moy"].round(2).astype(str) + "</b><br>"
    + "Victimes: <b>" + ville_agg["fatalities"].astype(str) + "</b><br>"
    + "Type dominant: <b>" + ville_agg["type_dominant"] + "</b>"
)

fig_map = go.Figure()
for evt_type, color in COLOR_MAP.items():
    if evt_type not in selected_types:
        continue
    sub = ville_agg[ville_agg["type_dominant"] == evt_type]
    if sub.empty:
        continue
    fig_map.add_trace(go.Scattermapbox(
        lat=sub["latitude"],
        lon=sub["longitude"],
        mode="markers",
        marker=dict(
            size=sub["total"].clip(3, 50),
            color=color,
            opacity=0.75,
            sizemode="area",
        ),
        text=sub["hover"],
        hovertemplate="%{text}<extra></extra>",
        name=evt_type,
    ))

fig_map.update_layout(
    mapbox=dict(
        style="carto-darkmatter",
        center=dict(lat=9.3, lon=2.3),
        zoom=6.2,
    ),
    height=520,
    paper_bgcolor="rgba(0,0,0,0)",
    legend=dict(bgcolor="rgba(13,15,26,0.8)", bordercolor="#252A48", borderwidth=1, font=dict(color="#C0C8E0")),
    margin=dict(l=0, r=0, t=30, b=0),
    title=dict(text="Cartographie des incidents – taille proportionnelle au nombre d'événements (survol pour détails)",
               font=dict(size=13, color="#8090C0")),
)
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")


# ─────────────────────────────────────────────────
# SECTION 5 – INDICE DE RÉACTIVITÉ
# ─────────────────────────────────────────────────
st.markdown("## ⚡ Indice de Réactivité — Ratio Action/Réaction")

st.markdown("""
<p style='color:#6070A0;font-size:0.85rem;'>
    <em>Signature d'expert :</em> Ce graphique compare l'évolution mensuelle des conflits (demande sécuritaire)
    et des coopérations (réponse institutionnelle). Un ratio &lt; 0.3 signale une sous-réactivité de l'État.
</p>
""", unsafe_allow_html=True)

df["mois_period"] = df["date"].dt.to_period("M").dt.to_timestamp()

conflits_mois = (
    df[df["event_type"].str.contains("Conflit")]
    .groupby("mois_period").size().reset_index(name="conflits")
)
coops_mois = (
    df[df["event_type"].str.contains("Coopération")]
    .groupby("mois_period").size().reset_index(name="coopérations")
)
reac = conflits_mois.merge(coops_mois, on="mois_period", how="outer").fillna(0)
reac["ratio"] = (reac["coopérations"] / reac["conflits"].replace(0, 1)).round(3)
reac = reac.sort_values("mois_period")

fig_reac = make_subplots(rows=2, cols=1, shared_xaxes=True,
                          row_heights=[0.65, 0.35],
                          vertical_spacing=0.08,
                          subplot_titles=("Flux Conflits vs Coopérations", "Ratio Réactivité Mensuel"))

fig_reac.add_trace(go.Bar(
    x=reac["mois_period"], y=reac["conflits"],
    name="Conflits", marker_color="#FF3A4A", marker_line_width=0,
    hovertemplate="%{x|%b %Y} — Conflits: <b>%{y}</b><extra></extra>",
), row=1, col=1)

fig_reac.add_trace(go.Bar(
    x=reac["mois_period"], y=reac["coopérations"],
    name="Coopérations", marker_color="#3A7EFF", marker_line_width=0,
    hovertemplate="%{x|%b %Y} — Coopérations: <b>%{y}</b><extra></extra>",
), row=1, col=1)

# Ratio en ligne avec coloration conditionnelle
ratio_colors = ["#30C080" if r >= 0.3 else "#FF9500" if r >= 0.1 else "#FF3A4A" for r in reac["ratio"]]
fig_reac.add_trace(go.Bar(
    x=reac["mois_period"], y=reac["ratio"],
    name="Ratio",
    marker_color=ratio_colors,
    marker_line_width=0,
    hovertemplate="%{x|%b %Y} — Ratio: <b>%{y:.3f}</b><extra></extra>",
), row=2, col=1)

# Ligne seuil 0.3
fig_reac.add_hline(y=0.3, line_dash="dash", line_color="#60D080", line_width=1.5,
                    annotation_text="Seuil acceptable (0.3)", annotation_font_color="#60D080",
                    row=2, col=1)
fig_reac.add_hline(y=0.05, line_dash="dot", line_color="#FF3A4A", line_width=1.5,
                    annotation_text="Seuil critique (0.05)", annotation_font_color="#FF3A4A",
                    row=2, col=1)

fig_reac.update_layout(
    barmode="group",
    height=500,
    **PLOTLY_THEME,
    showlegend=True,
    hovermode="x unified",
)
fig_reac.update_xaxes(gridcolor="#1E2240", linecolor="#2A3060")
fig_reac.update_yaxes(gridcolor="#1E2240", linecolor="#2A3060")

st.plotly_chart(fig_reac, use_container_width=True)

# Alerte ratio global
if ratio_reactivite < 0.05:
    st.error("🚨 **ALERTE MAXIMALE** : Capacité de réponse critique sur cette période. Le ratio de réactivité est inférieur au seuil critique de 0.05. Intervention urgente requise.")
elif ratio_reactivite < 0.1:
    st.warning(f"⚠️ **Zone Rouge** : Ratio de réactivité à **{ratio_reactivite:.3f}** — La réponse institutionnelle est très insuffisante face à la dynamique conflictuelle.")
elif ratio_reactivite < 0.3:
    st.warning(f"🟡 **Zone Orange** : Ratio de réactivité à **{ratio_reactivite:.3f}** — Des efforts de coopération sont présents mais restent insuffisants.")
else:
    st.success(f"✅ **Zone Verte** : Ratio de réactivité à **{ratio_reactivite:.3f}** — La réponse de l'État suit correctement l'évolution des conflits.")

st.markdown("---")


# ─────────────────────────────────────────────────
# SECTION 6 – ÉVÉNEMENTS CLÉS / INSIGHTS
# ─────────────────────────────────────────────────
st.markdown("## 🔍 Insights & Événements Clés")

col_i1, col_i2, col_i3 = st.columns(3)

with col_i1:
    st.markdown("### 🏆 Top 5 Villes Incidents")
    top_villes = df.groupby("ville").size().sort_values(ascending=False).head(5)
    for i, (ville, cnt) in enumerate(top_villes.items()):
        dept = df[df["ville"] == ville]["departement"].iloc[0]
        bar_pct = int(cnt / top_villes.max() * 100)
        st.markdown(f"""
        <div style='margin-bottom:10px;'>
            <div style='display:flex;justify-content:space-between;margin-bottom:3px;'>
                <span style='font-size:0.85rem;color:#C0C8E0;'><b>{i+1}.</b> {ville} <span style='color:#5A6A90;font-size:0.75rem;'>({dept})</span></span>
                <span style='font-family:IBM Plex Mono;font-size:0.85rem;color:#FF9500;'>{cnt}</span>
            </div>
            <div style='background:#1A1E35;border-radius:4px;height:4px;'>
                <div style='background:#FF9500;width:{bar_pct}%;height:100%;border-radius:4px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_i2:
    st.markdown("### 📊 Distribution Goldstein")
    fig_hist = go.Figure(go.Histogram(
        x=df["goldstein"], nbinsx=30,
        marker_color="#6C8EFF", marker_line_width=0,
        hovertemplate="Score: %{x:.1f}<br>Fréquence: %{y}<extra></extra>",
    ))
    fig_hist.add_vline(x=goldstein_moy, line_dash="dash", line_color="#FF4E5B",
                        annotation_text=f"Moy: {goldstein_moy:.2f}", annotation_font_color="#FF4E5B")
    fig_hist.add_vline(x=0, line_color="#30C080", line_width=1, opacity=0.5)
    fig_hist.update_layout(
        height=220, **PLOTLY_THEME,
        showlegend=False, margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(**PLOTLY_THEME["xaxis"], title="Score Goldstein"),
        yaxis=dict(**PLOTLY_THEME["yaxis"], title="Fréquence"),
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col_i3:
    st.markdown("### 🥧 Part des types")
    type_counts = df["event_type"].value_counts()
    fig_pie = go.Figure(go.Pie(
        labels=type_counts.index,
        values=type_counts.values,
        hole=0.55,
        marker_colors=[COLOR_MAP[t] for t in type_counts.index],
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>%{value} incidents (%{percent})<extra></extra>",
    ))
    fig_pie.update_layout(
        height=230, **PLOTLY_THEME,
        showlegend=True,
        legend=dict(**PLOTLY_THEME["legend"], orientation="v", font=dict(size=10)),
        margin=dict(l=0, r=0, t=10, b=10),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ─────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div style='text-align:center;color:#3A4070;font-size:0.75rem;font-family:IBM Plex Mono,monospace;padding:16px 0;'>
    🛡️ TABLEAU DE BORD TACTIQUE — ANALYSE DE CRISE BÉNIN 2025<br>
    Données simulées à des fins de démonstration · {total_incidents:,} événements analysés<br>
    Période : {selected_start.strftime('%d %b %Y')} → {selected_end.strftime('%d %b %Y')}
    &nbsp;|&nbsp; Départements sélectionnés : {len(selected_depts)}/{len(all_depts)}
</div>
""", unsafe_allow_html=True)