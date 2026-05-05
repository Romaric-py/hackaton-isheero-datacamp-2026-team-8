"""
=============================================================
  HACKATHON 2026 — Bénin Insights Challenge
  TABLEAU DE BORD TACTIQUE - ANALYSE DES INSIGHTS AU Bénin À PARTIR DES DONNÉES GDELT (12 DERNIERS MOIS)
  Focus : Stabilité, Conflits, Réactivité de l'État, Zones à Risque
=============================================================
"""

import warnings

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from dashboard.data_loader import load_dashboard_data
from dashboard.plot_utils import COLOR_MAP, hex_to_rgba, themed_layout
from dashboard.styles import apply_dashboard_styles

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

apply_dashboard_styles(st)

# ─────────────────────────────────────────────────
# CHARGEMENT DES DONNÉES
# ─────────────────────────────────────────────────
df_raw = load_dashboard_data()

# ─────────────────────────────────────────────────
# SIDEBAR – FILTRES
# ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
    <div style='text-align:center; padding: 12px 0 24px;'>
        <div style='font-family:Rajdhani;font-size:1.5rem;font-weight:700;
                    color:#FF4E5B;text-transform:uppercase;letter-spacing:3px;'>
             FILTRES ANALYTIQUES
        </div>
        <div style='font-size:0.7rem;color:#5060A0;letter-spacing:2px;margin-top:4px;'>
            ANALYSE DE CRISE · BÉNIN 2025
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("### 📅 Période d'analyse")
    date_min = df_raw["date"].min().date()
    date_max = df_raw["date"].max().date()

    all_months = sorted(df_raw["date"].dt.to_period("M").unique())
    month_labels = [str(m) for m in all_months]

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        start_idx = st.selectbox(
            "De",
            options=range(len(month_labels)),
            format_func=lambda i: month_labels[i],
            index=0,
        )
    with col_s2:
        end_idx = st.selectbox(
            "À",
            options=range(len(month_labels)),
            format_func=lambda i: month_labels[i],
            index=len(month_labels) - 1,
        )

    if start_idx > end_idx:
        st.warning("⚠️ Date de début > date de fin.")
        start_idx, end_idx = end_idx, start_idx

    selected_start = pd.Period(month_labels[start_idx], freq="M").start_time
    selected_end = pd.Period(month_labels[end_idx], freq="M").end_time

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
    st.caption(
        "💡 Tous les graphiques se mettent à jour en temps réel selon vos filtres."
    )


# ─────────────────────────────────────────────────
# FILTRAGE
# ─────────────────────────────────────────────────
if not selected_depts:
    selected_depts = all_depts
if not selected_types:
    selected_types = all_types

df = df_raw[
    (df_raw["date"] >= selected_start)
    & (df_raw["date"] <= selected_end)
    & (df_raw["departement"].isin(selected_depts))
    & (df_raw["event_type"].isin(selected_types))
].copy()


# ─────────────────────────────────────────────────
# EN-TÊTE
# ─────────────────────────────────────────────────
st.markdown(
    """
<div style='margin-bottom: 0;'>
    <h1 style='margin-bottom:0; font-family:sans-serif;'>
        HACKATHON 2026 — Bénin Insights Challenge
    </h1>
    <p style='color:#5A6A90; font-family:IBM Plex Mono, monospace; font-size:0.85rem; margin-top:4px; font-weight:bold; text-transform: uppercase;'>
        TABLEAU DE BORD TACTIQUE - ANALYSE DES INSIGHTS AU BÉNIN À PARTIR DES DONNÉES GDELT (12 DERNIERS MOIS)
    </p>
    <p style='color:#7B8694; font-family:IBM Plex Mono, monospace; font-size:0.75rem; margin-top:-10px;'>
        Focus : Stabilité, Conflits, Réactivité de l'État, Zones à Risque
    </p>
</div>
<hr style='margin-top:0;'>
""",
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────
# SECTION 1 – KPIs
# ─────────────────────────────────────────────────
st.markdown("## 📊 Chiffres Clés")

if df.empty:
    st.error("Aucune donnée pour les filtres sélectionnés.")
    st.stop()

total_incidents = len(df)
goldstein_moy = df["goldstein"].mean()
dept_le_plus_touche = (
    df[df["event_type"].str.contains("Conflit")]["departement"].value_counts().idxmax()
    if not df[df["event_type"].str.contains("Conflit")].empty
    else "N/A"
)
nb_conflits = df[df["event_type"].str.contains("Conflit")].shape[0]
nb_coops = df[df["event_type"].str.contains("Coopération")].shape[0]
ratio_reactivite = nb_coops / nb_conflits if nb_conflits > 0 else 0
total_fatalities = df["fatalities"].sum()

col1, col2, col3, col4, col5 = st.columns(5)

kpis = [
    (
        col1,
        total_incidents,
        "Incidents Totaux",
        "#FF4E5B",
        f"📍 {len(selected_depts)} depts",
    ),
    (
        col2,
        f"{goldstein_moy:.2f}",
        "Score de Stabilité",
        "#6C8EFF" if goldstein_moy >= 0 else "#FF4E5B",
        "Indice Goldstein moyen",
    ),
    (
        col3,
        dept_le_plus_touche,
        "Dept. le + Touché",
        "#FF9500",
        "Zone de conflit prioritaire",
    ),
    (
        col4,
        f"{ratio_reactivite:.2f}",
        "Ratio Réactivité",
        "#30C080",
        "Actions/Réactions État",
    ),
    (
        col5,
        int(total_fatalities),
        "Victimes Signalées",
        "#FF3A4A",
        "Total décès rapportés",
    ),
]

for col, val, label, accent, delta in kpis:
    with col:
        st.markdown(
            f"""
        <div class="kpi-card" style="--accent:{accent};">
            <div class="kpi-value">{val}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-delta">{delta}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ── Alertes dynamiques ─────────────────────────
alert_col1, alert_col2, alert_col3 = st.columns(3)

with alert_col1:
    if ratio_reactivite < 0.05:
        st.error(
            "⚠️ **Alerte Critique** : Capacité de réponse de l'État quasi-nulle sur cette période. Ratio réactivité < 0.05"
        )
    elif ratio_reactivite < 0.3:
        st.warning(
            f"⚡ **Réactivité Faible** : Le ratio Action/Réaction est de **{ratio_reactivite:.2f}**. La réponse institutionnelle reste insuffisante."
        )
    else:
        st.success(
            f"✅ **Réactivité Satisfaisante** : Ratio de **{ratio_reactivite:.2f}** — La réponse de l'État suit l'évolution des conflits."
        )

with alert_col2:
    pct_conflit = nb_conflits / total_incidents * 100 if total_incidents > 0 else 0
    if pct_conflit > 60:
        st.error(
            f"🔴 **Zone Rouge** : {pct_conflit:.0f}% des événements sont des conflits. Situation alarmante."
        )
    elif pct_conflit > 40:
        st.warning(
            f"🟡 **Zone de Tension** : {pct_conflit:.0f}% des événements sont conflictuels. Surveillance accrue recommandée."
        )
    else:
        st.info(
            f"🔵 **Zone Modérée** : {pct_conflit:.0f}% de conflits. Dynamique globalement stable."
        )

with alert_col3:
    if goldstein_moy < -3:
        st.error(
            f"📉 **Stabilité Critique** : Score Goldstein de **{goldstein_moy:.2f}**. Risque de déstabilisation élevé."
        )
    elif goldstein_moy < 0:
        st.warning(
            f"⚠️ **Instabilité Latente** : Score Goldstein de **{goldstein_moy:.2f}**. Tendance négative à surveiller."
        )
    else:
        st.success(
            f"📈 **Stabilité Positive** : Score Goldstein de **{goldstein_moy:.2f}**. Dynamique coopérative dominante."
        )

st.markdown("---")


# ─────────────────────────────────────────────────
# SECTION 2 – PANORAMA DE LA CRISE (Stacked Bar)
# ─────────────────────────────────────────────────
st.markdown("## 🏛️ Panorama de la Crise par Département")

dept_type = df.groupby(["departement", "event_type"]).size().reset_index(name="count")
dept_order = (
    dept_type[dept_type["event_type"].str.contains("Conflit")]
    .groupby("departement")["count"]
    .sum()
    .sort_values(ascending=False)
    .index.tolist()
)

fig_bar = go.Figure()
for evt_type, color in COLOR_MAP.items():
    if evt_type not in selected_types:
        continue
    data_t = dept_type[dept_type["event_type"] == evt_type]
    dept_counts = {r["departement"]: r["count"] for _, r in data_t.iterrows()}
    fig_bar.add_trace(
        go.Bar(
            name=evt_type,
            x=dept_order,
            y=[dept_counts.get(d, 0) for d in dept_order],
            marker_color=color,
            marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>" + evt_type + ": <b>%{y}</b><extra></extra>",
        )
    )

fig_bar.update_layout(
    barmode="stack",
    title=dict(
        text="Répartition des événements par département",
        font=dict(size=14, color="#8090C0"),
    ),
    height=400,
    **themed_layout(xaxis=dict(tickangle=-30)),
)
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")


# ─────────────────────────────────────────────────
# SECTION 3 – DYNAMIQUE TEMPORELLE
# ─────────────────────────────────────────────────
st.markdown("## 📈 Dynamique Temporelle des Incidents")

tab1, tab2 = st.tabs(
    ["📅 Évolution mensuelle (Line Chart)", "📊 Évolution hebdomadaire"]
)

with tab1:
    df["mois_period"] = df["date"].dt.to_period("M").dt.to_timestamp()
    monthly = df.groupby(["mois_period", "event_type"]).size().reset_index(name="count")

    fig_line = go.Figure()
    for evt_type, color in COLOR_MAP.items():
        if evt_type not in selected_types:
            continue
        sub = monthly[monthly["event_type"] == evt_type].sort_values("mois_period")
        fig_line.add_trace(
            go.Scatter(
                x=sub["mois_period"],
                y=sub["count"],
                name=evt_type,
                mode="lines+markers",
                line=dict(color=color, width=2.5),
                marker=dict(size=6, color=color, line=dict(color="#0D0F1A", width=1.5)),
                hovertemplate="<b>%{x|%b %Y}</b><br>"
                + evt_type
                + ": <b>%{y}</b><extra></extra>",
                fill="tozeroy",
                fillcolor=hex_to_rgba(color, 0.07) if color.startswith("#") else color,
            )
        )

    # Zone de pic décembre
    fig_line.add_vrect(
        x0="2025-11-01",
        x1="2025-12-31",
        fillcolor="rgba(255,60,74,0.06)",
        line_width=0,
        annotation_text="📍 Pic Q4",
        annotation_position="top left",
        annotation_font=dict(color="#FF4E5B", size=11),
    )

    fig_line.update_layout(
        title=dict(
            text="Évolution mensuelle des 4 grands types d'événements",
            font=dict(size=14, color="#8090C0"),
        ),
        height=420,
        **themed_layout(xaxis=dict(dtick="M1", tickformat="%b %Y")),
        hovermode="x unified",
    )
    st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    weekly = df.groupby(["semaine", "event_type"]).size().reset_index(name="count")
    fig_wk = go.Figure()
    for evt_type, color in COLOR_MAP.items():
        if evt_type not in selected_types:
            continue
        sub = weekly[weekly["event_type"] == evt_type].sort_values("semaine")
        fig_wk.add_trace(
            go.Bar(
                x=sub["semaine"],
                y=sub["count"],
                name=evt_type,
                marker_color=color,
                marker_line_width=0,
                hovertemplate="Semaine %{x}<br>"
                + evt_type
                + ": <b>%{y}</b><extra></extra>",
            )
        )
    fig_wk.update_layout(
        barmode="stack",
        title=dict(
            text="Activité hebdomadaire (par numéro de semaine ISO)",
            font=dict(size=14, color="#8090C0"),
        ),
        height=380,
        **themed_layout(xaxis=dict(title="Semaine de l'année")),
    )
    st.plotly_chart(fig_wk, use_container_width=True)

st.markdown("---")


# ─────────────────────────────────────────────────
# SECTION 4 – CARTOGRAPHIE TACTIQUE (Bubble Map)
# ─────────────────────────────────────────────────
st.markdown("## 🗺️ Cartographie Tactique — Points Chauds")

map_agg = (
    df.groupby(["ville", "departement", "event_type", "latitude", "longitude"])
    .agg(
        count=("goldstein", "count"),
        goldstein_moy=("goldstein", "mean"),
        fatalities=("fatalities", "sum"),
    )
    .reset_index()
)

# Agréger par ville tous types confondus pour la taille des bulles
ville_agg = (
    df.groupby(["ville", "departement", "latitude", "longitude"])
    .agg(
        total=("goldstein", "count"),
        goldstein_moy=("goldstein", "mean"),
        fatalities=("fatalities", "sum"),
    )
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
    "<b>"
    + ville_agg["ville"]
    + "</b> ("
    + ville_agg["departement"]
    + ")<br>"
    + "Incidents: <b>"
    + ville_agg["total"].astype(str)
    + "</b><br>"
    + "Goldstein moyen: <b>"
    + ville_agg["goldstein_moy"].round(2).astype(str)
    + "</b><br>"
    + "Victimes: <b>"
    + ville_agg["fatalities"].astype(str)
    + "</b><br>"
    + "Type dominant: <b>"
    + ville_agg["type_dominant"]
    + "</b>"
)

fig_map = go.Figure()
for evt_type, color in COLOR_MAP.items():
    if evt_type not in selected_types:
        continue
    sub = ville_agg[ville_agg["type_dominant"] == evt_type]
    if sub.empty:
        continue
    fig_map.add_trace(
        go.Scattermapbox(
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
        )
    )

fig_map.update_layout(
    mapbox=dict(
        style="carto-darkmatter",
        center=dict(lat=9.3, lon=2.3),
        zoom=6.2,
    ),
    height=520,
    paper_bgcolor="rgba(0,0,0,0)",
    legend=dict(
        bgcolor="rgba(13,15,26,0.8)",
        bordercolor="#252A48",
        borderwidth=1,
        font=dict(color="#C0C8E0"),
    ),
    margin=dict(l=0, r=0, t=30, b=0),
    title=dict(
        text="Cartographie des incidents – taille proportionnelle au nombre d'événements (survol pour détails)",
        font=dict(size=13, color="#8090C0"),
    ),
)
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")


# ─────────────────────────────────────────────────
# SECTION 5 – INDICE DE RÉACTIVITÉ
# ─────────────────────────────────────────────────
st.markdown("## ⚡ Indice de Réactivité — Ratio Action/Réaction")

st.markdown(
    """
<p style='color:#6070A0;font-size:0.85rem;'>
    <em>Signature d'expert :</em> Ce graphique compare l'évolution mensuelle des conflits (demande sécuritaire)
    et des coopérations (réponse institutionnelle). Un ratio &lt; 0.3 signale une sous-réactivité de l'État.
</p>
""",
    unsafe_allow_html=True,
)

df["mois_period"] = df["date"].dt.to_period("M").dt.to_timestamp()

conflits_mois = (
    df[df["event_type"].str.contains("Conflit")]
    .groupby("mois_period")
    .size()
    .reset_index(name="conflits")
)
coops_mois = (
    df[df["event_type"].str.contains("Coopération")]
    .groupby("mois_period")
    .size()
    .reset_index(name="coopérations")
)
reac = conflits_mois.merge(coops_mois, on="mois_period", how="outer").fillna(0)
reac["ratio"] = (reac["coopérations"] / reac["conflits"].replace(0, 1)).round(3)
reac = reac.sort_values("mois_period")

fig_reac = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    row_heights=[0.65, 0.35],
    vertical_spacing=0.08,
    subplot_titles=("Flux Conflits vs Coopérations", "Ratio Réactivité Mensuel"),
)

fig_reac.add_trace(
    go.Bar(
        x=reac["mois_period"],
        y=reac["conflits"],
        name="Conflits",
        marker_color="#FF3A4A",
        marker_line_width=0,
        hovertemplate="%{x|%b %Y} — Conflits: <b>%{y}</b><extra></extra>",
    ),
    row=1,
    col=1,
)

fig_reac.add_trace(
    go.Bar(
        x=reac["mois_period"],
        y=reac["coopérations"],
        name="Coopérations",
        marker_color="#3A7EFF",
        marker_line_width=0,
        hovertemplate="%{x|%b %Y} — Coopérations: <b>%{y}</b><extra></extra>",
    ),
    row=1,
    col=1,
)

# Ratio en ligne avec coloration conditionnelle
ratio_colors = [
    "#30C080" if r >= 0.3 else "#FF9500" if r >= 0.1 else "#FF3A4A"
    for r in reac["ratio"]
]
fig_reac.add_trace(
    go.Bar(
        x=reac["mois_period"],
        y=reac["ratio"],
        name="Ratio",
        marker_color=ratio_colors,
        marker_line_width=0,
        hovertemplate="%{x|%b %Y} — Ratio: <b>%{y:.3f}</b><extra></extra>",
    ),
    row=2,
    col=1,
)

# Ligne seuil 0.3
fig_reac.add_hline(
    y=0.3,
    line_dash="dash",
    line_color="#60D080",
    line_width=1.5,
    annotation_text="Seuil acceptable (0.3)",
    annotation_font_color="#60D080",
    row=2,
    col=1,
)
fig_reac.add_hline(
    y=0.05,
    line_dash="dot",
    line_color="#FF3A4A",
    line_width=1.5,
    annotation_text="Seuil critique (0.05)",
    annotation_font_color="#FF3A4A",
    row=2,
    col=1,
)

fig_reac.update_layout(
    barmode="group",
    height=500,
    **themed_layout(showlegend=True, hovermode="x unified"),
)
fig_reac.update_xaxes(gridcolor="#1E2240", linecolor="#2A3060")
fig_reac.update_yaxes(gridcolor="#1E2240", linecolor="#2A3060")

st.plotly_chart(fig_reac, use_container_width=True)

# Alerte ratio global
if ratio_reactivite < 0.05:
    st.error(
        "🚨 **ALERTE MAXIMALE** : Capacité de réponse critique sur cette période. Le ratio de réactivité est inférieur au seuil critique de 0.05. Intervention urgente requise."
    )
elif ratio_reactivite < 0.1:
    st.warning(
        f"⚠️ **Zone Rouge** : Ratio de réactivité à **{ratio_reactivite:.3f}** — La réponse institutionnelle est très insuffisante face à la dynamique conflictuelle."
    )
elif ratio_reactivite < 0.3:
    st.warning(
        f"🟡 **Zone Orange** : Ratio de réactivité à **{ratio_reactivite:.3f}** — Des efforts de coopération sont présents mais restent insuffisants."
    )
else:
    st.success(
        f"✅ **Zone Verte** : Ratio de réactivité à **{ratio_reactivite:.3f}** — La réponse de l'État suit correctement l'évolution des conflits."
    )

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
        st.markdown(
            f"""
        <div style='margin-bottom:10px;'>
            <div style='display:flex;justify-content:space-between;margin-bottom:3px;'>
                <span style='font-size:0.85rem;color:#C0C8E0;'><b>{i + 1}.</b> {ville} <span style='color:#5A6A90;font-size:0.75rem;'>({dept})</span></span>
                <span style='font-family:IBM Plex Mono;font-size:0.85rem;color:#FF9500;'>{cnt}</span>
            </div>
            <div style='background:#1A1E35;border-radius:4px;height:4px;'>
                <div style='background:#FF9500;width:{bar_pct}%;height:100%;border-radius:4px;'></div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

with col_i2:
    st.markdown("### 📊 Distribution Goldstein")
    fig_hist = go.Figure(
        go.Histogram(
            x=df["goldstein"],
            nbinsx=30,
            marker_color="#6C8EFF",
            marker_line_width=0,
            hovertemplate="Score: %{x:.1f}<br>Fréquence: %{y}<extra></extra>",
        )
    )
    fig_hist.add_vline(
        x=goldstein_moy,
        line_dash="dash",
        line_color="#FF4E5B",
        annotation_text=f"Moy: {goldstein_moy:.2f}",
        annotation_font_color="#FF4E5B",
    )
    fig_hist.add_vline(x=0, line_color="#30C080", line_width=1, opacity=0.5)
    fig_hist.update_layout(
        height=220,
        **themed_layout(
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(title="Score Goldstein"),
            yaxis=dict(title="Fréquence"),
        ),
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col_i3:
    st.markdown("### 🥧 Part des types")
    type_counts = df["event_type"].value_counts()
    fig_pie = go.Figure(
        go.Pie(
            labels=type_counts.index,
            values=type_counts.values,
            hole=0.55,
            marker_colors=[COLOR_MAP[t] for t in type_counts.index],
            textinfo="percent",
            hovertemplate="<b>%{label}</b><br>%{value} incidents (%{percent})<extra></extra>",
        )
    )
    fig_pie.update_layout(
        height=230,
        **themed_layout(
            showlegend=True,
            legend=dict(orientation="v", font=dict(size=10)),
            margin=dict(l=0, r=0, t=10, b=10),
        ),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ─────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    f"""
<div style='text-align:center;color:#3A4070;font-size:0.75rem;font-family:IBM Plex Mono,monospace;padding:16px 0;'>
    🛡️ TABLEAU DE BORD TACTIQUE — ANALYSE DE CRISE BÉNIN 2025<br>
    Données simulées à des fins de démonstration · {total_incidents:,} événements analysés<br>
    Période : {selected_start.strftime("%d %b %Y")} → {selected_end.strftime("%d %b %Y")}
    &nbsp;|&nbsp; Départements sélectionnés : {len(selected_depts)}/{len(all_depts)}
</div>
""",
    unsafe_allow_html=True,
)
