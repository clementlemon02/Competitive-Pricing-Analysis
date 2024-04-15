import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from components import navbar

# Import Open Sans Font for those that is not using it
app = Dash(__name__, use_pages=True, external_stylesheets=['https://fonts.googleapis.com/css2?family=Lora:wght@400;700&display=swap', dbc.themes.BOOTSTRAP,'styles.css'],suppress_callback_exceptions=True)


app.layout = html.Div(children=[
    dcc.Location(id="url"),
    navbar, 
   dbc.Container([
    dash.page_container
    ],
    id="page-content",
    fluid=True
   )
])#, style={'zoom':'85%'}) # Set zoom to 85% to accommodate small screens

if __name__ == '__main__':
    app.run_server(debug=True)
