COLOR_MAP = {
    "Conflit Matériel": "#FF3A4A",
    "Conflit Verbal": "#FF9500",
    "Coopération Matérielle": "#3A7EFF",
    "Coopération Verbale": "#30C080",
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


def themed_layout(**overrides):
    layout = {**PLOTLY_THEME}
    for axis_key in ("xaxis", "yaxis", "legend"):
        if (
            axis_key in overrides
            and isinstance(layout.get(axis_key), dict)
            and isinstance(overrides[axis_key], dict)
        ):
            layout[axis_key] = {**layout[axis_key], **overrides[axis_key]}
            overrides.pop(axis_key)
    layout.update(overrides)
    return layout


def hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip("#")
    red = int(hex_color[0:2], 16)
    green = int(hex_color[2:4], 16)
    blue = int(hex_color[4:6], 16)
    return f"rgba({red},{green},{blue},{alpha})"
