import dash_bootstrap_components as dbc
from dash import html, callback, Input, Output


# CSS styles for navbar
nav_text_default = {'color': '#3A3B3C', 'text-align': 'center'}
nav_text_selected = {'color': '#FFFFFF', 'text-align': 'center'}
nav_button_default = {'border-style': 'solid', 'border-color': '#F0AA06', 'margin-right': '15px', 'width': '150px', 'border-radius': '25px',
                      'border-width': 'medium'}
nav_button_selected = {'border-style': 'solid', 'border-color': '#8ABA3D', 'margin-right': '15px', 'width': '150px', 'border-radius': '25px',
                       'background-color': '#046845', 'border-width': 'medium'}


# Create Navigation Bar
navbar = dbc.Navbar(
    dbc.Container(
        [
            # Create Logo and Brand flushed to the left
            dbc.Row(
                dbc.Col([
                    html.Img(src='/assets/mlfg_logo.png', height="85px"),
                    dbc.NavbarBrand("Mount Faber Leisure Group")
                    ])
                    ),

            # Create navigation buttons flushed to the right
            dbc.Row(
                dbc.Col(
                    dbc.Nav([
                        dbc.NavItem(dbc.NavLink("Introduction", href="/", id="intro_text"),
                                    id="intro_button"),
                        dbc.NavItem(dbc.NavLink("Dashboard", href="/data-visualisation", id="data_text"),
                                    id="data_button"),
                        dbc.NavItem(dbc.NavLink("Simulation", href="/pricing-simulation", id="pricing_text"),
                                    id="pricing_button")
                    ])
                )
            )
        ],
      #  style={'font-size': '18px', 'height': 'auto', 'background-color': '#fafafa'},
        fluid=True
    )
)


# Define the callback to highlight active button
@callback(
    [Output("intro_text", "style"),
     Output("data_text", "style"),
     Output("pricing_text", "style"),
     Output("intro_button", "style"),
     Output("data_button", "style"),
     Output("pricing_button", "style"),
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
