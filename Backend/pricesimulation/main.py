from .model import SkyHelixModel
import matplotlib.pyplot as plt
import numpy as np
from mesa.batchrunner import batch_run
import pandas as pd
import json



##def run_simulation(object):
def run_simulation(data):
        
    model = SkyHelixModel(num_passengers = data['input_number_of_passengers'],
                          initial_ticket_price = data['input_initial_ticket_price'],
                          competitors_price = data['input_competitors_price'],
                        )

    # Run the model for a fixed number of steps
    for i in np.arange(10):  
        model.step()

    # Access model data and visualize results
    optimized_parameters = model.get_optimized_parameters()
    print("Average Competitor Price:", "S$", round(model.average_competitor_price,2))
    print("Optimized Ticket Price:", "S$", round(optimized_parameters["Optimized_Ticket_Price"],2))
    print("Expected Passengers:", optimized_parameters["Expected_Passengers"])
    print("Expected Revenue:", "S$", round(round(optimized_parameters["Optimized_Ticket_Price"], 2) * optimized_parameters["Expected_Passengers"],2))
    print("Tickets Purchased:", optimized_parameters["Tickets_Purchased"])
    print("Tickets Not Purchased:", optimized_parameters["Tickets_Not_Purchased"])

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

    # by front end
    # we need to return the optimization parameter to diaplay it on the webpage
    return optimized_parameters

if __name__ == "__main__":
    # Example usage
    test_data = {
        'input_number_of_passengers': 10000,
        'input_initial_ticket_price': 20,
        'input_competitors_price': [10, 30, 48, 49.5, 30, 23, 45.6, 12, 40, 42, 34.05, 40, 45.6]
    }
    run_simulation(test_data)
