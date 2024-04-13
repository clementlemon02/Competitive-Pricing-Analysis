from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agent import PassengerAgent
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class SkyHelixModel(Model):
    def __init__(self, num_passengers, initial_ticket_price,competitors_price, grid_width, grid_height):
        super().__init__()
        self.num_passengers = num_passengers
        self.ticket_price = initial_ticket_price
        self.competitors_price = competitors_price
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.demographic_densities = {
            "Adult": 0.5,
            "Senior": 0.2,
            "Student": 0.3
        }
        self.total_revenue = 0
        self.total_tickets_sold = 0
        self.grid = MultiGrid(self.grid_width, self.grid_height, True)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            agent_reporters={"Ticket_Purchased": lambda a: a.ticket_purchased}
        )
        self.create_agents()

    def create_agents(self):
        # Now use self.demographic_densities directly
        total_density = sum(self.demographic_densities.values())
        for demographic, density in self.demographic_densities.items():
            num_agents = int(self.num_passengers * (density / total_density))
            for i in range(num_agents):
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                agent = PassengerAgent(i, self, demographic)
                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)


          # if base price > max price

    def step(self):
        # Adjust the ticket price based on optimization strategy
        self.optimize_ticket_price()

        # Step through the model and collect data
        self.schedule.step()
        self.datacollector.collect(self)

    def optimize_ticket_price(self):
    # Calculate the current demand as the number of agents willing to purchase tickets at the current price
      demand = sum(agent.ticket_purchased for agent in self.schedule.agents)

    # Adjust the ticket price based on demand
      if demand > self.num_passengers / 2:
        self.ticket_price += 1  # Increase price if demand is high
      elif demand < self.num_passengers / 4:
        self.ticket_price -= 1  # Decrease price if demand is low

    # Calculate revenue based on the current ticket price and demand
      self.total_revenue = self.ticket_price * demand  # Corrected to match actual demand

    # Update the total number of tickets sold
      self.total_tickets_sold = demand  # Corrected to reflect actual purchases

    # def optimize_ticket_price(self):
    #     total_demand = 0
    #     for agent in self.schedule.agents:
    #         if agent.demographic == "Family":
    #             total_demand += agent.num_individuals if agent.ticket_purchased else 0
    #         else:
    #             total_demand += 1 if agent.ticket_purchased else 0

    #     # Adjust ticket price based on demand
    #     if total_demand > self.num_passengers / 2:
    #         self.ticket_price += 1  # Increase price if demand is high
    #     elif total_demand < self.num_passengers / 4:
    #         self.ticket_price -= 1  # Decrease price if demand is low

    #     # Calculate revenue based on the current ticket price and total demand
    #     self.total_revenue = self.ticket_price * total_demand

    #     # Update the total number of tickets sold
    #     self.total_tickets_sold = total_demand



    def get_ticket_counts(self):
    # Count the number of tickets purchased
      tickets_purchased = sum(agent.ticket_purchased for agent in self.schedule.agents)
      tickets_not_purchased = self.num_passengers - tickets_purchased

      return tickets_purchased, tickets_not_purchased

    def get_optimized_parameters(self):
    # Include ticket purchase counts directly in the optimized parameters
      tickets_purchased, tickets_not_purchased = self.get_ticket_counts()
      optimized_parameters = {
        "Optimized_Ticket_Price": self.ticket_price,
        "Expected_Passengers": tickets_purchased,  # This now directly reflects tickets purchased
        "Expected_Revenue": self.total_revenue,
        "Tickets_Purchased": tickets_purchased,
        "Tickets_Not_Purchased": tickets_not_purchased
    }

      return optimized_parameters


    def calculate_utility_threshold(self, target_revenue):
        # You can define the utility threshold based on various factors, such as target revenue, costs, etc.
        # For example, you can set the utility threshold as a percentage of the target revenue.
        # Feel free to adjust this calculation based on your specific requirements.

        # You might want to adjust this calculation based on your specific requirements
        utility_threshold = target_revenue * 0.1  # 10% of the target revenue

        # Adjust the threshold based on the average utility
        # For example, you can make it proportional to the average utility
        average_utility = np.mean(self.get_utility_values())
        utility_threshold *= average_utility / 10  # Adjust based on the average utility

        return utility_threshold


    def calculate_utility_threshold(self, target_revenue):
        # You can define the utility threshold based on various factors, such as target revenue, costs, etc.
        # For example, you can set the utility threshold as a percentage of the target revenue.
        # Feel free to adjust this calculation based on your specific requirements.

        # You might want to adjust this calculation based on your specific requirements
        utility_threshold = target_revenue * 0.1  # 10% of the target revenue

        # Adjust the threshold based on the average utility
        # For example, you can make it proportional to the average utility
        average_utility = np.mean(self.get_utility_values())
        utility_threshold *= average_utility / 10  # Adjust based on the average utility

        return utility_threshold

    
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

    def plot_utility_vs_price(self):
        utility_price_pairs = self.get_utility_and_price()
        prices, utilities = zip(*utility_price_pairs)

        plt.figure(figsize=(8, 6))
        plt.scatter(utilities, prices, alpha=0.5)
        plt.xlabel('utility')
        plt.ylabel('Ticket Price')
        plt.title('Utility vs. Ticket Price')
        plt.grid(True)
        plt.show()

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
        sns.kdeplot(utilities, shade=True, color="r")
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
