import dash_bootstrap_components as dbc
from dash import html, callback, Input, Output


# CSS styles for navbar
nav_text_default = {'color': '#3A3B3C', 'text-align': 'center'}
nav_text_selected = {'color': '#FFFFFF', 'text-align': 'center'}
nav_button_default = {'border-style': 'solid', 'margin-right': '15px', 'width': '150px', 'border-radius': '25px',
                      'border-width': 'medium'}
nav_button_selected = {'border-style': 'solid', 'margin-right': '15px', 'width': '150px', 'border-radius': '25px',
                       'background-color': '#333333', 'border-width': 'medium'}

# Create Navigation Bar
navbar = dbc.Navbar(
    dbc.Container(
        [
            # Create Logo and Brand flushed to the left
            dbc.Row(
                dbc.Col([
                    #html.Img(src=app.get_asset_url('nus_logo.svg'), height="72px", style={"padding": "10px"}),
                    dbc.NavbarBrand("Mount Faber Group",
                                    style={'font-weight': 'bold', 'font-size': '35px', 'color': '#3A3B3C',
                                           'padding-left': '30px', 'vertical-align': 'middle'})
                ])
            ),

            # Create navigation buttons flushed to the right
            dbc.Row(
                dbc.Col(
                    dbc.Nav([
                        dbc.NavItem(dbc.NavLink("Introduction", href="/", id="intro_text"),
                                    id="intro_button"),
                        dbc.NavItem(dbc.NavLink("Visualisation", href="/data-visualisation", id="data_text"),
                                    id="data_button"),
                        dbc.NavItem(dbc.NavLink("Simulation", href="/pricing-simulation", id="pricing_text"),
                                    id="pricing_button")
                    ])
                )
            )
        ],
        style={'font-family': 'Open Sans', 'font-size': '18px', 'height': 'auto', 'background-color': '#d3d3d3'},
        fluid=True
    ),
    style={'padding': '0px'}  # set to 0 else will have white space
)

# Define the callback to highlight active button
@callback(
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
