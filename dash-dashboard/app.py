import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

#Import navbar from separate modules
from components import navbar

# Import Open Sans Font for those that is not using it
app = Dash(__name__, use_pages=True, external_stylesheets=['https://fonts.googleapis.com/css?family=Open+Sans:400,600', dbc.themes.BOOTSTRAP])

# Register the pages
#dash.register_page(__name__)

'''# CSS styles for navbar
nav_text_default = {'color':'#3A3B3C', 'text-align':'center'}
nav_text_selected = {'color':'#FFFFFF','text-align':'center'}
nav_button_default = {'border-style': 'solid', 'margin-right':'15px','width':'150px','border-radius': '25px','border-width':'medium'}
nav_button_selected = {'border-style': 'solid','margin-right':'15px','width':'150px','border-radius': '25px','background-color':'#333333', 'border-width':'medium'}

# Create a callback to highlight the active navigation button
@app.callback(
    [Output("intro_text", "style"),
     Output("data_text", "style"),
     Output("pricing_text", "style"),
     Output("intro_button", "style"),
     Output("data_button", "style"),
     Output("pricing_button", "style")
     ],
    [Input("url", "pathname")]
)
def highlight_active_button(pathname):
    if pathname == "/":
        return nav_text_selected, nav_text_default, nav_text_default, nav_button_selected, nav_button_default, nav_button_default
    elif pathname == "/data-visualisation":
        return nav_text_default, nav_text_selected, nav_text_default, nav_button_default, nav_button_selected, nav_button_default
    elif pathname == "/pricing-simulation":
        return nav_text_default, nav_text_default, nav_text_selected, nav_button_default, nav_button_default, nav_button_selected

#Create Navigation Bar
navbar = dbc.Navbar(
            dbc.Container(
                [
                    # Create Logo and Brand flushed to the left
                    dbc.Row(
                        dbc.Col([
                            html.Img(src=dash.get_asset_url('nus_logo.svg'), height="72px", style={"padding":"10px"}),
                            dbc.NavbarBrand("Mount Faber Group", style={'font-weight':'bold','font-size':'35px','color':'#3A3B3C','padding-left':'30px','vertical-align':'middle'})
                        ])
                    ),

                    # Create navigation buttons flushed to the right
                    dbc.Row(      
                        dbc.Col(
                            dbc.Nav([
                                dbc.NavItem(dbc.NavLink("Introduction", href="/introduction", id="intro_text"), id="intro_button"),
                                dbc.NavItem(dbc.NavLink("Visualisation", href="/data-visualisation", id="data_text"), id="data_button"),
                                dbc.NavItem(dbc.NavLink("Simulation", href="/pricing-simulation", id="pricing_text"), id="pricing_button")
                            ])
                        )
                    )
                ], 
                style={'font-family': 'Open Sans', 'font-size': '18px', 'height':'auto','background-color':'#d3d3d3'},
                fluid=True
            ), 
            style={'padding':'0px'} #set to 0 else will have white space
) '''

app.layout = html.Div(children=[
    dcc.Location(id="url"),
    navbar, 
   dbc.Container([
				dash.page_container
				],
				id="page-content",
				fluid=True
			)
], style={'zoom':'85%'}) # Set zoom to 75% to accommodate small screens



if __name__ == '__main__':
    app.run(debug=True)
