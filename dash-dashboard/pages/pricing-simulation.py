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
import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import requests
import json
from dash.exceptions import PreventUpdate

dash.register_page(__name__) 


layout = html.Div([
    html.H1("Dynamic Simulation Display"),
    html.Div([  
        html.P("Number of Visitors:", style={'display': 'inline-block', 'margin-right': '10px'}),  
        dcc.Input(id="input-number-of-passengers", type="number", value=10000,style={'fontFamily': 'Lora'}),  
    ], style={'margin-bottom': '10px'}),  
    html.Div([  
        html.P("Initial Ticket Price (S$):", style={'display': 'inline-block', 'margin-right': '10px'}),  
        dcc.Input(id="input-initial-ticket-price", type="number", value=20, style={'fontFamily': 'Lora'}),  
    ], style={'margin-bottom': '10px'}),
    html.Button("Run Simulation", id="run-simulation-button", n_clicks=0,  className="nav-text-selected nav-button-selected", style={'margin-bottom': '20px'}),
    dcc.Interval(id='update-interval', interval=1000, n_intervals=0, disabled=True),  # Disabled initially
    dcc.Store(id='simulation-data-store'),  # To store simulation data
    dcc.Store(id='current-step', data={'step': 0}),  # To store current step index
    html.Div(id="simulation-output"),
    html.Div(id="simulation-results"),  # Div to display results and plots
])

@callback(
    [Output('simulation-data-store', 'data'),
     Output('update-interval', 'disabled')],
    Input('run-simulation-button', 'n_clicks'),
    [State('input-number-of-passengers', 'value'),
     State('input-initial-ticket-price', 'value')],
    prevent_initial_call=True
)
def fetch_simulation_data(n_clicks, num_passengers, initial_ticket_price):
    if n_clicks == 0:
        raise PreventUpdate

    input_competitors_price = [10, 30, 48, 49.5, 30, 23, 45.6, 12, 40, 42, 34.05, 40, 45.6]
    input_data = {
        'input_number_of_passengers': num_passengers,
        'input_initial_ticket_price': initial_ticket_price,
        "input_competitors_price": input_competitors_price
    }
    response = requests.post('http://127.0.0.1:5000/pricing-simulation', json=input_data)
    if response.status_code == 200:
        data = response.json()
        return data, False  # Enable interval updates
    return {}, True  # Keep interval disabled on failure

@callback(
    Output('simulation-output', 'children'),
    Output('current-step', 'data'),
    Input('update-interval', 'n_intervals'),
    State('simulation-data-store', 'data'),
    State('current-step', 'data')
)
def update_simulation_visualization(n_intervals, simulation_data, current_step_data):
    if not simulation_data:
        raise PreventUpdate

    current_step = current_step_data['step'] 
    grid_state = simulation_data['grid_state'][current_step]

    purchased_x = [cell['x'] for cell in grid_state if cell['purchased']]
    purchased_y = [cell['y'] for cell in grid_state if cell['purchased']]
    not_purchased_x = [cell['x'] for cell in grid_state if not cell['purchased']]
    not_purchased_y = [cell['y'] for cell in grid_state if not cell['purchased']]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=purchased_x, y=purchased_y, mode='markers', marker=dict(color='green', size=10), name='Purchased'))
    fig.add_trace(go.Scatter(x=not_purchased_x, y=not_purchased_y, mode='markers', marker=dict(color='red', size=10), name='Not Purchased'))
    fig.update_layout(title=f'Step {current_step}', xaxis=dict(range=[-1, 100]), yaxis=dict(range=[-1, 100]),paper_bgcolor = '#f7ffea')

    current_step += 1
    if current_step >= len(simulation_data['grid_state']):
        current_step = 0  # Reset to loop

    return dcc.Graph(figure=fig), {'step': current_step }

@callback(
    Output('simulation-results', 'children'),
    Input('simulation-data-store', 'data')
)
def display_simulation_results(simulation_data):
    if not simulation_data:
        raise PreventUpdate
    
    # Extract results data
    results = simulation_data.get('optimized_parameters', {})
    
    '''
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
    '''

    # Generate a summary HTML layout
    return html.Div([
        html.H2("Simulation Summary"),
        html.P(f"Optimized Ticket Price: ${results.get('Optimized_Ticket_Price', 'N/A'):.0f}"),
        html.P(f"Expected Passengers: {results.get('Expected_Passengers', 'N/A')}"),
        html.P(f"Expected Revenue: ${results.get('Expected_Revenue', 'N/A'):.0f}"),
        html.P(f"Tickets Purchased: {results.get('Tickets_Purchased', 'N/A')}"),
        html.P(f"Tickets Not Purchased: {results.get('Tickets_Not_Purchased', 'N/A')}"),
        html.H2("Competitor Prices Considered by the Model",style={'margin-bottom':'20px'}),  
        html.Div([  
            html.P([
                    'Gardens by the Bay',
                    html.Span(' - Floral Fantasy: Singaopre Residents ', style={'font-style': 'italic'}), 
                    html.Span(' S$10', style={'font-weight': 'bold'})
                    ]),
            html.P([
                    'Gardens by the Bay',
                    html.Span(' - Cloud Forest + Flower Dome + Floral Fantasy: Singapore Residents ', style={'font-style': 'italic'}), 
                    html.Span(' S$30', style={'font-weight': 'bold'})
                    ]),
            html.P([
                    'Gardens by the Bay',                        
                    html.Span(' - Flower Dome + Supertree Observatory + Floral Fantasy: Non-Residents ', style={'font-style': 'italic'}), 
                    html.Span(' S$48', style={'font-weight': 'bold'})
                    ]),
            html.P([                  
                    'Night Safari Singapore',                        
                    html.Span(' - Admission Ticket + Tram Ride: Singapore Residents ', style={'font-style': 'italic'}),  
                    html.Span(' S$49.50', style={'font-weight': 'bold'})
                    ]),
            html.P([
                    'Marina Bay Sands Skypark',                        
                    html.Span(' - Marina Bay Sands Skypark: Non-Peak Hour Tickets ', style={'font-style': 'italic'}), 
                    html.Span(' S$30', style={'font-weight': 'bold'})
                    ]),
            html.P([
                    'ArtScience Museum',                        
                    html.Span(' - Mars : The red mirror tickets ', style={'font-style': 'italic'}), 
                    html.Span(' S$23', style={'font-weight': 'bold'})
                    ]),
            html.P([
                    'Singapore Zoo',                        
                    html.Span(' - Admission Ticket + Tram Ride: Singapore Residents ', style={'font-style': 'italic'}), 
                    html.Span(' S$45.60', style={'font-weight': 'bold'})
                    ]),                
            html.P([                        
                    'Snow City',
                    html.Span(' - 1-Hour Play Session ', style={'font-style': 'italic'}), 
                    html.Span(' S$12', style={'font-weight': 'bold'})
                    ]),
            html.P([
                    'Adventure Cove Waterpark',
                    html.Span(' - Admission tickets ', style={'font-style': 'italic'}), 
                    html.Span(' S$40', style={'font-weight': 'bold'})
                    ]),
            html.P([
                    'River Wonders Singapore',
                    html.Span(' - Singapore Residents ', style={'font-style': 'italic'}), 
                    html.Span(' S$42', style={'font-weight': 'bold'})
                    ]),
            html.P([
                    'Skyline Luge Sentoas',
                    html.Span(' - Luge & Skyride: 2 Rounds + Luge Branded Merchandise ', style={'font-style': 'italic'}), 
                    html.Span(' S$34.05', style={'font-weight': 'bold'})
                    ]),
            html.P([
                    'Resorts World Sentosa',
                    html.Span(' - Admission Tickets ', style={'font-style': 'italic'}), 
                    html.Span(' S$40', style={'font-weight': 'bold'})
                    ]),
            html.P([
                    'Mantai Wildlife Reserve',
                    html.Span(' - Admission Ticket + Tram Ride: Singapore Residents ', style={'font-style': 'italic'}), 
                    html.Span(' S$45.60', style={'font-weight': 'bold'})
                    ])
        ])
    ], style={'padding': '20px', 'border': '1px solid #ccc', 'border-radius': '5px', 'margin-top': '20px'})
    
    


'''
        html.Div([  
                    html.H2("Ticket Sales Simulation"),  
                    html.P("Projected ticket sales"),  
                    html.Div([dcc.Graph(id='ticket-purchase-chart', figure=fig)]),  
                ],className='col-md-6', style={'margin-bottom': '20px'}),
'''