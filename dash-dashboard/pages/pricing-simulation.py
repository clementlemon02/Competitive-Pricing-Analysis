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


dash.register_page(__name__)

# Define the layout for the pricing simulation page
layout = html.Div([
    html.H2("Pricing Simulation"),
    html.Label("Number of Passengers:"),
    dcc.Input(id="input-number-of-passengers", type="number", value=10000),
    html.Label("Initial Ticket Price (S$):"),
    dcc.Input(id="input-initial-ticket-price", type="number", value=20),
    html.Label("Competitors' Prices (S$, separated by comma):"),
    dcc.Input(id="input-competitors-price", type="text", placeholder="10, 30, 48, ..."),
    html.Button("Run Simulation", id="run-simulation-button", n_clicks=0, className="mt-3"),
    html.Div(id="simulation-output")
], className="mt-3")

'''
# Callback to run simulation and display output
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

    competitors_price = [float(price.strip()) for price in competitors_price.split(',')]
    test_data = {
        'input_number_of_passengers': num_passengers,
        'input_initial_ticket_price': initial_ticket_price,
        'input_competitors_price': competitors_price
    }
    model_output = run_simulation(test_data)
    # You can modify this to display any specific output from the model if needed
    return html.Div([
        html.H2("Simulation Results"),
        html.Pre(json.dumps(model_output, indent=4)),
        # Add any additional components to display here (e.g., charts)
    ])
'''

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
    # You can modify this to display any specific output from the model if needed

    # Access model data and visualize results
    #optimized_parameters = model_output['optimized_parameters']
    #average_competitor_price = model_output['average_competitor_price']
    
    # Construct HTML to display model output
    output_html = html.Div([
        html.H2("Simulation Results"),
        #html.P(f"Average Competitor Price: S$ {round(average_competitor_price, 2)}"),
        html.P(f"Optimized Ticket Price: S$ {round(model_output['Optimized_Ticket_Price'], 2)}"),
        html.P(f"Expected Passengers: {model_output['Expected_Passengers']}"),
        html.P(f"Expected Revenue: S$ {round(round(model_output['Optimized_Ticket_Price'], 2) * model_output['Expected_Passengers'], 2)}"),
        html.P(f"Tickets Purchased: {model_output['Tickets_Purchased']}"),
        html.P(f"Tickets Not Purchased: {model_output['Tickets_Not_Purchased']}")
    ])

    return output_html
