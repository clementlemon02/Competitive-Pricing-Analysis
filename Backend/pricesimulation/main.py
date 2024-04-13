from model import SkyHelixModel
import matplotlib.pyplot as plt
import numpy as np
from mesa.batchrunner import batch_run
import pandas as pd
import json



##def run_simulation(object):
def run_simulation(data):
        
    model = SkyHelixModel(num_passengers = data['input_number_of_passengers'],
                          initial_ticket_price=data['input_initial_price'],
                          competitors_price=data['input_competitors_price'],
                          grid_width=1, grid_height=1)

    # Run the model for a fixed number of steps
    for i in np.arange(10):  
        model.step()

    # Access model data and visualize results
    optimized_parameters = model.get_optimized_parameters()
    print("Optimized Ticket Price:", optimized_parameters["Optimized_Ticket_Price"])
    print("Expected Passengers:", optimized_parameters["Expected_Passengers"])
    print("Expected Revenue:", optimized_parameters["Expected_Revenue"])
    print("Tickets Purchased:", optimized_parameters["Tickets_Purchased"])
    print("Tickets Not Purchased:", optimized_parameters["Tickets_Not_Purchased"])

    model.plot_utility_vs_price()
    model.plot_utility()


    # Extract the data from the DataCollector
    data = model.datacollector.get_agent_vars_dataframe()

    # Create a bar chart to show the number of agents who purchased tickets and those who didn't
    plt.bar(['Purchased Tickets', 'Did Not Purchase Tickets'], [optimized_parameters["Tickets_Purchased"], optimized_parameters["Tickets_Not_Purchased"]])

    # Set the title and labels for the chart
    plt.title('Ticket Purchase Distribution')
    plt.xlabel('Ticket Status')
    plt.ylabel('Number of Agents')

    # Display the chart
    plt.show()

if __name__ == "__main__":
    # Example usage
    test_data = {
        'input_number_of_passengers': 10000,
        'input_initial_price': 30,
        'input_competitors_price': 20
    }
    run_simulation(test_data)
