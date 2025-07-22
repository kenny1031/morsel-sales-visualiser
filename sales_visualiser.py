from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd

# Load preprocessed CSV file
df = pd.read_csv("pink_morsel_sales.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

COLOURS = {  # Adobe‑Color palette #45488A
    "primary": "#45488A",
    "secondary": "#1C1C62",
    "font": "#FFFFFF",
    "curve": "#F6ED79"
}

# Initialise dash
app = Dash(__name__)

# Create the figure
def generate_figure(fig_data):
    fig = px.line(
        fig_data,
        x="date",
        y="sales",
        color="region",
        labels={"date": "Date", "sales": "Sales ($)"},
        title="Pink Morsel Sales",
    )
    fig.update_layout(
        plot_bgcolor=COLOURS["secondary"],
        paper_bgcolor=COLOURS["primary"],
        font_color=COLOURS["font"],
    )
    return fig

# region picker
region_picker = dcc.RadioItems(
    ["all", "north", "east", "south", "west"],
    "all",
    labelStyle={"color": COLOURS["font"]},
    id="region_picker",
    inline=True
)
region_picker_wrapper = html.Div(
    children=[region_picker],
    style={"font-size": "150%"}
)

# Define the app layout
app.layout = html.Div(
    children=[
        html.H1(
            "Pink Morsel Visualiser",
            id="header",
            style={
                "background-color": COLOURS["secondary"],
                "color": COLOURS["font"],
                "border-radius": "20px"
            }
        ),
        dcc.Graph(
            id="graph",
            figure=generate_figure(df)
        ),
        region_picker_wrapper,
        html.H3(
            children="Price‑rise checkpoint (15 Jan 2021)",
            style={
                "textAlign": "left",
                "color": COLOURS["font"]
            },
        ),
        html.Div(
            id="before-after",
            style={
                "textAlign": "left",
                "color": COLOURS["font"]
            },
        )
    ],
    style={
        "textAlign": "center",
        "background-color": COLOURS["primary"],
        "border-radius": "20px"
    },
)

# Callbacks
@app.callback(
    Output("graph", "figure"),
    Output("before-after", "children"),
    Input(region_picker, "value"),
)
def update_visual(selected_region: str):
    # Filter view by region
    if selected_region == "all":
        view = df
    else:
        view = df[df["region"] == selected_region]
    # Build the figure
    figure = generate_figure(view)

    # Average sales before/after 15‑Jan‑2021
    cutoff = pd.Timestamp("2021-01-15")
    before_avg = view.loc[view["date"] < cutoff, "sales"].mean()
    after_avg = view.loc[view["date"] >= cutoff, "sales"].mean()
    verdict = (
        "higher after the price rise" if after_avg > before_avg else "higher before the price rise"
    )
    interp = (
        f"Average sales before 15 Jan 2021 was ${before_avg:,.0f}, "
        f"after was ${after_avg:,.0f}. Hence, the sales was {verdict}."
    )
    return figure, interp


if __name__ == "__main__":
    app.run(debug=True)
