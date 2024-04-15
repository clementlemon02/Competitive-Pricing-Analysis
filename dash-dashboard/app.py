import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

#Import navbar from separate modules
#from '../Backend/pricesimulation/main' import run_simulation
#from '../Backend/pricesimulation/model' import SkyHelixModel
from components import navbar

# Import Open Sans Font for those that is not using it
<<<<<<< Updated upstream
app = Dash(__name__, use_pages=True, external_stylesheets=['https://fonts.googleapis.com/css2?family=Lora:wght@400;700&display=swap', dbc.themes.BOOTSTRAP])
=======
app = Dash(__name__, use_pages=True, external_stylesheets=['https://fonts.googleapis.com/css2?family=Lora:wght@400;700&display=swap', dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
>>>>>>> Stashed changes

app.layout = html.Div(children=[
    dcc.Location(id="url"),
    navbar, 
   dbc.Container([
<<<<<<< Updated upstream
				dash.page_container
				],
				id="page-content",
				fluid=True
			)
=======
    dash.page_container
    ],
    id="page-content",
    fluid=True
   )
>>>>>>> Stashed changes
])#, style={'zoom':'85%'}) # Set zoom to 85% to accommodate small screens


if __name__ == '__main__':
    app.run(debug=True)


