import dash_bootstrap_components as dbc
from dash import html, callback, Input, Output

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
                        dbc.NavItem(dbc.NavLink("Introduction", href="/", id="intro_text", className="nav-text-default"),
                                    id="intro_button", className="nav-button-default"),
                        dbc.NavItem(dbc.NavLink("Visualisation", href="/data-visualisation", id="data_text", className="nav-text-default"),
                                    id="data_button", className="nav-button-default"),
                        dbc.NavItem(dbc.NavLink("Simulation", href="/pricing-simulation", id="pricing_text", className="nav-text-default"),
                                    id="pricing_button", className="nav-button-default")
                    ])
                )
            )
        ],
        fluid=True
    )
)

# Define the callback to highlight active button
@callback(
    [Output("intro_text", "className"),
    Output("data_text", "className"),
    Output("pricing_text", "className"),
    Output("intro_button", "className"),
    Output("data_button", "className"),
    Output("pricing_button", "className")],
    [Input("url", "pathname")]
)
def highlight_active_button(pathname):
    if pathname == "/":
        return "nav-text-selected", "nav-text-default", "nav-text-default", "nav-button-selected", "nav-button-default", "nav-button-default"
    elif pathname == "/data-visualisation":
        return "nav-text-default", "nav-text-selected", "nav-text-default", "nav-button-default",  "nav-button-selected", "nav-button-default"
    elif pathname == "/pricing-simulation":
        return "nav-text-default", "nav-text-default", "nav-text-selected", "nav-button-default", "nav-button-default",  "nav-button-selected"