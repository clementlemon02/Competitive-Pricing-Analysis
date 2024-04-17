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
import requests 

dash.register_page(__name__) 

# Define the layout for the pricing simulation page 
layout = html.Div([ 
    html.H1("Pricing Simulation for SkyHelix"), 
    html.P("Please key in your input below."), 
    html.Div([ 
        html.Div("Number of Visitors:", style={'display': 'inline-block', 'margin-right': '10px'}), 
        dcc.Input(id="input-number-of-passengers", type="number", value=10000), 
    ], style={'margin-bottom': '10px'}), 
    html.Div([ 
        html.Div("Initial Ticket Price (S$):", style={'display': 'inline-block', 'margin-right': '10px'}), 
        dcc.Input(id="input-initial-ticket-price", type="number", value=20), 
    ], style={'margin-bottom': '10px'}), 
    html.Button("Run Simulation", id="run-simulation-button", n_clicks=0,  className="nav-text-selected nav-button-selected", style={'margin-bottom': '20px'}), 
    html.Div(id="simulation-output") 
]) 

@callback( 
    Output('simulation-output', 'children'), 
    [Input('run-simulation-button', 'n_clicks')], 
    [State('input-number-of-passengers', 'value'), 
     State('input-initial-ticket-price', 'value')] 
    ) 
 
def run_simulation(n_clicks, num_passengers, initial_ticket_price):
    if n_clicks == 0: 
        raise PreventUpdate 
     
    input_data = {
        'input_number_of_passengers': num_passengers, 
        'input_initial_ticket_price': initial_ticket_price, 
        'input_competitors_price': [10, 30, 48, 49.5, 30, 23, 45.6, 12, 40, 42, 34.05, 40, 45.6]
        } 
 
    response = requests.post('http://127.0.0.1:5000/pricing-simulation', json=input_data) 
    if response.status_code == 200: 
        output = response.json()
        output_data = output['optimized_parameters'] 
        grid_state = output['grid_state'][0] 
 
        # Create a bar chart trace 
        bar_chart_trace = go.Bar( 
        x=['Purchased Tickets', 'Did Not Purchase Tickets'], 
        y=[output_data["Tickets_Purchased"], output_data["Tickets_Not_Purchased"]], 
        marker=dict(color=['#046845']) 
        ) 
 
        # Create layout for the bar chart 
        layout = go.Layout( 
        plot_bgcolor='#E6FAD5', 
        font=dict(family='Lora', size=18), 
        xaxis=dict(title='Ticket Status',tickfont=dict(family='Lora', size=14)), 
        yaxis=dict(title='Number of Agents',tickfont=dict(family='Lora', size=14)), 
        height=700, 
        width=700
        ) 
 
        # Create a figure object 
        fig = go.Figure(data=[bar_chart_trace], layout=layout) 
 
        #function to create a grid
        def create_grid_figure(grid_state): 
            # Convert grid state to x, y, and color 
            x = [cell['x'] for cell in grid_state] 
            y = [cell['y'] for cell in grid_state] 
            colors = ['#046845' if cell['purchased'] else 'black' for cell in grid_state] 
 
            trace = go.Scatter( 
                x=x, 
                y=y, 
                mode='markers', 
                marker=dict(color=colors, size=8)  # Adjust size as necessary 
            ) 
 
            layout = go.Layout( 
                plot_bgcolor='#E6FAD5', 
                font=dict(family='Lora', size=18), 
                xaxis=dict(title='X', tickmode='linear', dtick=10), 
                yaxis=dict(title='Y', tickmode='linear', dtick=10), 
                height=700, 
                width=700, 
            ) 
 
            return go.Figure(data=[trace], layout=layout) 
         
        grid_fig = create_grid_figure(grid_state) 
 
        output_html = html.Div([
            html.H1("Simulation Results", style={'margin-bottom': '20px'}), 
            html.Div([ 
                #Grid Simulation 
                html.Div([ 
                    html.H2("Grid Simulation"), 
                    html.P("Green represents agents that purchased a ticket, and black represents those that did not."), 
                    html.Div([dcc.Graph(id='grid-chart', figure=grid_fig)]), 
                ], className="col-md-6", style={'margin-bottom': '20px'}), 
                # Ticket Sales Simulation 
                html.Div([ 
                    html.H2("Ticket Sales Simulation"), 
                    html.P("Projected ticket sales"), 
                    html.Div([dcc.Graph(id='ticket-purchase-chart', figure=fig)]), 
                ],className='col-md-6', style={'margin-bottom': '20px'}), 
            ],className='row'), 
            html.H2("Summary",style={'margin-bottom':'20px'}), 
                    html.Div([ 
                        html.P(f"Optimized Ticket Price: S$ {round(output_data['Optimized_Ticket_Price'], 2)}"), 
                        html.P(f"Expected Passengers: {output_data['Expected_Passengers']}"), 
                        html.P(f"Expected Revenue: S$ {round(output_data['Expected_Revenue'], 2)}"), 
                        html.P(f"Tickets Purchased: {output_data['Tickets_Purchased']}"), 
                        html.P(f"Tickets Not Purchased: {output_data['Tickets_Not_Purchased']}"),
                        ], style={'margin-bottom': '50px'}),
            html.H2("Competitor Prices Considered by the Model",style={'margin-bottom':'20px'}), 
                    html.Div([ 
                        html.P("Gardens by the Bay - Floral Fantasy: Singapore Residents  S$10"),
                        html.P("Gardens by the Bay - Cloud Forest + Flower Dome + Floral Fantasy: Singapore Residents  S$30"),
                        html.P("Gardens by the Bay - Flower Dome + Supertree Observatory + Floral Fantasy: Non-Residents  S$48"),
                        html.P("Night Safari Singapore - Admission Ticket + Tram Ride: Singapore Residents  S$49.50"),
                        html.P("Marina Bay Sands Skypark - Marina Bay Sands Skypark: Non-Peak Hour Tickets  S$30"),
                        html.P("ArtScience Museum - Mars : The red mirror tickets  S$23"),
                        html.P("Singapore Zoo - Admission Ticket + Tram Ride: Singapore Residents  S$45.60"),
                        html.P("Snow City - 1-Hour Play Session  S$12"),
                        html.P("Adventure Cove Waterpark - Admission Tickets  S$40"),
                        html.P("River Wonders Singapore - Singapore Residents  S$42"),
                        html.P("Skyline Luge Sentosa - Luge & Skyride: 2 Rounds + Luge Branded Merchandise  S$34.05"),
                        html.P("Resorts World Sentosa - Admission Tickets  S$40"),
                        html.P("Mandai Wildlife Reserve - Admission Ticket + Tram Ride: Singapore Residents  S$45.60")
                        ]) 
        ])
 
        return output_html 
    else: 
        return html.Div((f"Error: {response.status_code} - {response.text}")) 
        return html.Div("Error running simulation")