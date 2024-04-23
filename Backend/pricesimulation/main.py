from .model import SkyHelixModel
import numpy as np
import json
import math
import random

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(sys.path)

def run_simulation(data):
    input_grid_width = input_grid_height = math.ceil(math.sqrt(data['input_number_of_passengers']))   
    model = SkyHelixModel(num_passengers = data['input_number_of_passengers'],
                          initial_ticket_price = data['input_initial_ticket_price'],
                          competitors_price = data['input_competitors_price'],
                          grid_width = input_grid_width,
                          grid_height = input_grid_height
                        )
    grid_state = []
    ticket_prices = []
    agents = model.schedule.agents

    # Set all agents' purchased status to False initially
    initial_state = [
        {"x": agent.pos[0], "y": agent.pos[1], "purchased": False}
        for agent in agents
    ]

    # Randomly select one agent to set 'purchased' to True
    random_agent_index = random.randint(0, len(agents) - 1)
    initial_state[random_agent_index]['purchased'] = True

    # Add initial state to the grid state list
    grid_state.append(initial_state)
    ticket_prices.append(0)

    # Run the model for a fixed number of steps
    for i in np.arange(10):  
        model.step()
        # Capture Grid State
        step_state = [
        {"x": agent.pos[0], 
         "y": agent.pos[1], 
         "purchased": agent.ticket_purchased}
        for agent in model.schedule.agents
        ]
        grid_state.append(step_state)
        ticket_prices.append(model.ticket_price)

    optimized_parameters = model.get_optimized_parameters()
    return {"optimized_parameters": optimized_parameters, "grid_state": grid_state, "ticket_prices": ticket_prices}

if __name__ == "__main__":
    # Example usage
    test_data = {
        'input_number_of_passengers': 10000,
        'input_initial_ticket_price': 20,
        'input_competitors_price': [10, 30, 48, 49.5, 30, 23, 45.6, 12, 40, 42, 34.05, 40, 45.6],
        'input_grid_width': 100,
        'input_grid_height': 100
    }
    run_simulation(test_data)