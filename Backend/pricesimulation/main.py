from .model import SkyHelixModel
# from model import SkyHelixModel
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from mesa.batchrunner import batch_run
import pandas as pd
import json
import math

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

    # Run the model for a fixed number of steps
    for i in np.arange(10):  
        model.step()

    # Access model data and visualize results
    optimized_parameters = model.get_optimized_parameters()
    # print("Average Competitor Price:", "S$", round(model.average_competitor_price,2))
    # print("Optimized Ticket Price:", "S$", round(optimized_parameters["Optimized_Ticket_Price"],2))
    # print("Expected Passengers:", optimized_parameters["Expected_Passengers"])
    # print("Expected Revenue:", "S$", round(round(optimized_parameters["Optimized_Ticket_Price"], 2) * optimized_parameters["Expected_Passengers"],2))
    # print("Tickets Purchased:", optimized_parameters["Tickets_Purchased"])
    # print("Tickets Not Purchased:", optimized_parameters["Tickets_Not_Purchased"])

    # model.plot_utility()


    # # Extract the data from the DataCollector
    # data = model.datacollector.get_agent_vars_dataframe()

    ## by front end: we need to add a return statement to print this out at the webpage
    return optimized_parameters

'''
instead of a pop out window, we will transfer this code to the frontend code to display the plot in the html webpage
    # Create a bar chart to show the number of agents who purchased tickets and those who didn't
    plt.bar(['Purchased Tickets', 'Did Not Purchase Tickets'], [optimized_parameters["Tickets_Purchased"], optimized_parameters["Tickets_Not_Purchased"]])

    # Set the title and labels for the chart
    plt.title('Ticket Purchase Distribution')
    plt.xlabel('Ticket Status')
    plt.ylabel('Number of Agents')

    # Display the chart
    plt.show()
'''



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
