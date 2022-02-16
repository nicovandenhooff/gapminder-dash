import numpy as np
import pandas as pd
import altair as alt

from dash import Dash, html, dcc, Input, Output

# Read in global data
url = "https://raw.githubusercontent.com/UofTCoders/workshops-dc-py/master/data/processed/world-data-gapminder.csv"
gapminder = pd.read_csv(url)

# Wrangle data
gapminder = gapminder.dropna()
gapminder["log_income"] = gapminder["income"].apply(np.log)

# Stylesheet
stylesheet = "https://codepen.io/chriddyp/pen/bWLwgP.css"

# Setup app and layout/frontend
app = Dash(__name__, external_stylesheets=[stylesheet])

app.layout = html.Div(
    [
        html.Iframe(
            id="bubble_chart",
            style={"border-width": "0", "width": "100%", "height": "400px"},
        ),
        dcc.Slider(
            min=1970,
            max=2010,
            step=5,
            value=2010,
            id="year_widget",
            marks={i: str(i) for i in range(1970, 2015, 5)},
        ),
    ]
)


# Set up callbacks/backend
@app.callback(Output("bubble_chart", "srcDoc"), Input("year_widget", "value"))
def plot_altair(year):
    chart = (
        alt.Chart(gapminder.query("year == @year"), title="Income vs. Life Expectancy")
        .mark_circle()
        .encode(
            alt.X(
                "log_income", title="Income (Log Scale)", scale=alt.Scale(zero=False)
            ),
            alt.Y(
                "life_expectancy",
                title="Life Expectancy (Years)",
                scale=alt.Scale(zero=False),
            ),
            alt.Size(
                "population", title="Population", scale=alt.Scale(range=(10, 1000))
            ),
            alt.Color("region", title="Continent"),
        )
        .configure_axis(titleFontSize=14)
    )

    return chart.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)
