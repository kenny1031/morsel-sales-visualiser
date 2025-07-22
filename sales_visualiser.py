from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd

# Load preprocessed CSV file
df = pd.read_csv("pink_morsel_sales.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Dash layout
COLORWAY = ["#EF476F", "#FF7E8C", "#FFB3C0", "#2F2F33"]  # Adobe‑Color palette
BG_SOFT   = "#FFF3F6"

external_stylesheets = [
    "https://fonts.googleapis.com/css?family=Nunito:wght@300;400;600&display=swap",
]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    className="container",
    children=[
        html.H1("Pink Morsel Sales Dashboard", className="title"),

        # ── Region selector ─────────────────────────────────────────────
        dcc.RadioItems(
            id="region-filter",
            options=[
                {"label": "All Regions", "value": "all"},
                {"label": "North",       "value": "north"},
                {"label": "East",        "value": "east"},
                {"label": "South",       "value": "south"},
                {"label": "West",        "value": "west"},
            ],
            value="all",
            inline=True,
            className="radio-bar",
        ),

        # ── Line chart ──────────────────────────────────────────────────
        dcc.Graph(id="sales-line"),

        html.H3("Price‑rise checkpoint (15 Jan 2021)"),
        html.Div(id="before-after"),
    ],
)

# Callbacks
@app.callback(
    Output("sales-line", "figure"),
    Output("before-after", "children"),
    Input("region-filter", "value"),
)
def update_visual(selected_region: str):
    # Filter view by region
    if selected_region == "all":
        view = df.copy()
        title_suffix = "— All Regions"
        colour_arg = "region"
    else:
        view = df[df["region"] == selected_region]
        title_suffix = f"— {selected_region.capitalize()}"
        colour_arg = None  # single‑line series

    # Build the figure
    fig = px.line(
        view,
        x="date",
        y="sales",
        color=colour_arg,
        labels={"date": "Date", "sales": "Sales ($)"},
        title=f"Daily Pink Morsel Sales {title_suffix}",
        color_discrete_sequence=COLORWAY,
    )
    fig.update_layout(
        legend_title_text="Region",
        plot_bgcolor=BG_SOFT,
        paper_bgcolor=BG_SOFT,
        margin=dict(l=30, r=30, t=60, b=40),
    )

    # Average sales before/after 15‑Jan‑2021
    cutoff = pd.Timestamp("2021-01-15")
    before_avg = view.loc[view["date"] < cutoff, "sales"].mean()
    after_avg = view.loc[view["date"] >= cutoff, "sales"].mean()
    verdict = (
        "higher after the price rise" if after_avg > before_avg else "higher before the price rise"
    )
    blurb = (
        f"Average sales before 15 Jan 2021 was ${before_avg:,.0f}, "
        f"after was ${after_avg:,.0f}. Hence, the sales was {verdict}."
    )

    return fig, blurb


if __name__ == "__main__":
    app.run(debug=True)
