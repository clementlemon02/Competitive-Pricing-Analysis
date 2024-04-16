import dash
from dash import html, Input, Output, State, callback,dcc
import json
from dash.exceptions import PreventUpdate
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
parent_dir = os.path.abspath(os.path.join(parent_dir, '..'))
sys.path.insert(0, parent_dir)
from Backend.pricesimulation.main import run_simulation
import plotly.graph_objects as go

dash.register_page(__name__)



# Define the layout for the pricing simulation page
layout = html.Div([
    html.H1("Pricing Simulation"),
    html.P("Please Key in your input below."),
    html.Div([
        html.Div("Number of Visitors:", style={'display': 'inline-block', 'margin-right': '10px'}),
        dcc.Input(id="input-number-of-passengers", type="number", value=10000),
    ], style={'margin-bottom': '10px'}),
    html.Div([
        html.Div("Initial Ticket Price (S$):", style={'display': 'inline-block', 'margin-right': '10px'}),
        dcc.Input(id="input-initial-ticket-price", type="number", value=20),
    ], style={'margin-bottom': '10px'}),
    html.Div([
        html.Div("Competitors' Prices (S$, separated by comma):", style={'display': 'inline-block', 'margin-right': '10px'}),
        dcc.Input(id="input-competitors-price", type="text", placeholder="10, 30, 48, ..."),
    ], style={'margin-bottom': '10px'}),
    html.Button("Run Simulation", id="run-simulation-button", n_clicks=0, className="nav-text-selected nav-button-selected", style={'margin-bottom': '20px'}),
    html.Div(id="simulation-output")
])


@callback(
    Output('simulation-output', 'children'),
    [Input('run-simulation-button', 'n_clicks')],
    [State('input-number-of-passengers', 'value'),
     State('input-initial-ticket-price', 'value'),
     State('input-competitors-price', 'value')]
)
def run_and_display_simulation(n_clicks, num_passengers, initial_ticket_price, competitors_price):
    if n_clicks == 0:
        raise PreventUpdate

    if competitors_price is None:
        competitors_price = ""

    competitors_price = [float(price.strip()) for price in competitors_price.split(',') if price.strip()]
    
    test_data = {
        'input_number_of_passengers': num_passengers,
        'input_initial_ticket_price': initial_ticket_price,
        'input_competitors_price': competitors_price
    }
    model_output = run_simulation(test_data)

    # Access model data and visualize results
    optimized_parameters = model_output['optimized_parameters']
    grid_state = model_output['grid_state']
    
    # Create a bar chart trace
    bar_chart_trace = go.Bar(
    x=['Purchased Tickets', 'Did Not Purchase Tickets'],
    y=[optimized_parameters["Tickets_Purchased"], optimized_parameters["Tickets_Not_Purchased"]],
    marker=dict(color=['#046845'])
    )

    # Create layout for the bar chart
    layout = go.Layout(
    plot_bgcolor='#E6FAD5',
    font=dict(family='Lora', size=18),
    title='Ticket Purchase Distribution',
    xaxis=dict(title='Ticket Status',tickfont=dict(family='Lora', size=14)),
    yaxis=dict(title='Number of Agents',tickfont=dict(family='Lora', size=14)),
    )

    # Create a figure object
    fig = go.Figure(data=[bar_chart_trace], layout=layout)

    # Construct HTML to display model output
    output_html = html.Div([
        html.Div(),
        html.H1("Simulation Results"),
        html.Div(),
        # html.P(f"Average Competitor Price: S$ {round(average_competitor_price, 2)}"),
        html.P(f"Optimized Ticket Price: S$ {round(optimized_parameters['Optimized_Ticket_Price'], 2)}"),
        html.P(f"Expected Passengers: {optimized_parameters['Expected_Passengers']}"),
        html.P(f"Expected Revenue: S$ {round(round(optimized_parameters['Optimized_Ticket_Price'], 2) * optimized_parameters['Expected_Passengers'], 2)}"),
        html.P(f"Tickets Purchased: {optimized_parameters['Tickets_Purchased']}"),
        html.P(f"Tickets Not Purchased: {optimized_parameters['Tickets_Not_Purchased']}"),
        html.Div([dcc.Graph(id='ticket-purchase-chart', figure=fig)])
    ])

    return output_html



