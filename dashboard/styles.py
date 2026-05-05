APP_CSS = """
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
"""


def apply_dashboard_styles(st):
    st.markdown(APP_CSS, unsafe_allow_html=True)
