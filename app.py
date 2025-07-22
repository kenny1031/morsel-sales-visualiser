from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd

# Load preprocessed CSV file
df = pd.read_csv("pink_morsel_sales.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Create line chart figure
fig = px.line(
    df,
    x="date",
    y="sales",
    color="region",
    title="Daily Pink Morsel Sales",
    labels={
        "date": "Date",
        "sales": "Sales ($)"
    }
)

# Dash layout
app = Dash(__name__)
app.layout = html.Div(
    style={"maxWidth": 900, "margin": "auto"},
    children=[
        html.H1(children="Pink Morsel Sales Dashboard", style={"textAlign": "center"}),
        dcc.Graph(
            id="sales-line-graph",
            figure=fig
        ),
        html.H3(children="Price-rise checkpoint (15 Jan 2021)"),
        html.Div(id="before-after")
    ]
)

# Simple callback -> prices before and after 15 Jan 2021
@app.callback(
    Output("before-after", "children"),
    Input("sales-line-graph", "figure")
)
def compare_sales(_):
    cutoff = pd.Timestamp("2021-01-15")
    before = df.loc[df["date"] < cutoff, "sales"].mean()
    after = df.loc[df["date"] >= cutoff, "sales"].mean()
    verdict = "higher after the price rise" \
        if after > before else \
        "higher before the price rise"
    output = f"Average sales before 15 Jan 2021 was ${before:,.0f}, "
    output += f"after was ${after:,.0f}  →  the sales was {verdict}."
    return output


if __name__ == "__main__":
    app.run(debug=True)
