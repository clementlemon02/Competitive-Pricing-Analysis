from mesa import Agent, Model
from mesa.space import MultiGrid, SingleGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from .agent import PassengerAgent
# from agent import PassengerAgent
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import random

class SkyHelixModel(Model):
    def __init__(self, num_passengers, initial_ticket_price,competitors_price, grid_width, grid_height):
        super().__init__()
        self.num_passengers = num_passengers
        self.ticket_price = initial_ticket_price
        self.initial_ticket_price = initial_ticket_price
        self.competitors_price = competitors_price
        self.average_competitor_price = 0
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.demographic_densities = {
            "Adult": 0.5,
            "Senior": 0.2,
            "Student": 0.3
        }
        self.total_revenue = 0
        self.total_tickets_sold = 0
        # self.grid = MultiGrid(self.grid_width, self.grid_height, True)
        self.grid = SingleGrid(self.grid_width, self.grid_height, True)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            agent_reporters={"Ticket_Purchased": lambda a: a.ticket_purchased}
        )
        self.create_agents()

    # def create_agents(self):
    #     # Now use self.demographic_densities directly
    #     total_density = sum(self.demographic_densities.values())
    #     for demographic, density in self.demographic_densities.items():
    #         num_agents = int(self.num_passengers * (density / total_density))
    #         for i in range(num_agents):
    #             x = self.random.randrange(self.grid.width)
    #             y = self.random.randrange(self.grid.height)
    #             agent = PassengerAgent(i, self, demographic)
    #             self.grid.place_agent(agent, (x, y))
    #             self.schedule.add(agent)

    def create_agents(self):
        # Create a list of all possible coordinates on the grid
        all_coordinates = [(x, y) for x in range(self.grid.width) for y in range(self.grid.height)]
        random.shuffle(all_coordinates)  # Shuffle the list randomly

        # Iterate through demographic densities
        total_density = sum(self.demographic_densities.values())
        for demographic, density in self.demographic_densities.items():
            num_agents = int(self.num_passengers * (density / total_density))
            
            # Assign unique coordinates to each agent
            for i in range(num_agents):
                if all_coordinates:
                    # Pop a coordinate from the shuffled list
                    x, y = all_coordinates.pop()
                else:
                    # If no more unique coordinates available, break the loop
                    break
                
                # Create and place the agent
                agent = PassengerAgent(i, self, demographic)
                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)

    def step(self):
        self.optimize_ticket_price()
        self.calculate_average_competitor_price()
        self.schedule.step()
        self.datacollector.collect(self)

    def calculate_average_competitor_price(self):
        if self.schedule.agents:
            self.average_competitor_price = np.mean([agent.model.competitors_price for agent in self.schedule.agents])


    def optimize_ticket_price(self):
      # Use a feedback loop from market conditions
      if self.ticket_price > self.average_competitor_price:
        self.ticket_price *= (1 - 0.02)  # Adjust down if above average
      elif self.ticket_price < self.average_competitor_price:
        self.ticket_price *= (1 + 0.02)  # Adjust up if below average

      # Maintain bounds
      self.ticket_price = max(min(self.ticket_price, self.initial_ticket_price * 2), self.initial_ticket_price * 0.5)

      demand = sum(agent.ticket_purchased for agent in self.schedule.agents)
      self.total_revenue = self.ticket_price * demand  # Corrected to match actual demand


    def get_ticket_counts(self):
    # Count the number of tickets purchased
      tickets_purchased = sum(agent.ticket_purchased for agent in self.schedule.agents)
      tickets_not_purchased = self.num_passengers - tickets_purchased

      return tickets_purchased, tickets_not_purchased

    def get_optimized_parameters(self):
    # Include ticket purchase counts directly in the optimized parameters
      tickets_purchased, tickets_not_purchased = self.get_ticket_counts()
      optimized_parameters = {
        "Optimized_Ticket_Price": round(self.ticket_price,2),
        "Expected_Passengers": tickets_purchased,  # This now directly reflects tickets purchased
        "Expected_Revenue": round(round(self.ticket_price,2)*tickets_purchased,2),
        "Tickets_Purchased": tickets_purchased,
        "Tickets_Not_Purchased": tickets_not_purchased
    }

      return optimized_parameters

    def get_utility_values(self):
      utility_values = []
      for agent in self.schedule.agents:
          utility = agent.calculate_utility()
          utility_values.append(utility)
      return utility_values

    def get_utility_and_price(self):
        utility_price_pairs = []
        for agent in self.schedule.agents:
            utility = agent.calculate_utility()
            price = self.ticket_price  # Assuming you have a way to access the ticket price
            utility_price_pairs.append((price, utility))
        return utility_price_pairs

    def plot_utility(self):
        utilities = self.get_utility_values()
        plt.figure(figsize=(24, 6))  # Widen the figure to accommodate three plots

        # Plot 1: Scatter plot of utilities
        plt.subplot(1, 3, 1)  # 1 row, 3 columns, 1st subplot
        plt.scatter(range(len(utilities)), utilities, alpha=0.5)
        plt.xlabel('Agent Index')
        plt.ylabel('Utility')
        plt.title('Utility Values of Agents')
        plt.grid(True)

        # Plot 2: Histogram of utilities
        plt.subplot(1, 3, 2)  # 1 row, 3 columns, 2nd subplot
        plt.hist(utilities, bins=20, alpha=0.7, color='blue')
        plt.xlabel('Utility')
        plt.ylabel('Frequency')
        plt.title('Histogram of Utility Values')

        # Plot 3: Density plot of utilities
        plt.subplot(1, 3, 3)  # 1 row, 3 columns, 3rd subplot
        sns.kdeplot(utilities, fill=True, color="r")
        plt.xlabel('Utility')
        plt.ylabel('Density')
        plt.title('Density Plot of Utility Values')

        plt.tight_layout()  # Adjust subplot params
        plt.show()

        # Calculate and print mean and standard deviation of utilities
        mean_utility = np.mean(utilities)
        std_utility = np.std(utilities)
        num_of_utility = len(utilities)

        print(f"Mean Utility: {mean_utility:}")
        print(f"Standard Deviation of Utility: {std_utility:}")
        print(f"Number of Utility Values: {num_of_utility}")