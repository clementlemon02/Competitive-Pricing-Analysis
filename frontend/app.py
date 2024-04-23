import dash 
from dash import Dash, html, dcc, Input, Output 
import dash_bootstrap_components as dbc 
from components import navbar 

from pages import introduction
from pages import data_visualisation
from pages import pricing_simulation
from dash import register_page
 
# Import Open Sans Font for those that is not using it 
app = Dash(__name__, external_stylesheets=['https://fonts.googleapis.com/css2?family=Lora:wght@400;700&display=swap', dbc.themes.BOOTSTRAP,'styles.css'],suppress_callback_exceptions=True) 

# Define the app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

register_page(__name__, path='/', title='Introduction', view_func=lambda: introduction)
register_page(__name__, path='/pricing-simulation', title='Introduction', view_func=lambda: pricing_simulation)
register_page(__name__, path='/', title='data-visualisation', view_func=lambda: data_visualisation)


# Update page content based on router
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return introduction.layout
    elif pathname == '/pricing-simulation':
        return pricing_simulation.layout
    elif pathname == '/data-visualisation':
        return data_visualisation.layout


if __name__ == '__main__': 
    app.run_server(debug=True)