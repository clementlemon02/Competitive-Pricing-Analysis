import numpy as np
import random
from mesa import Agent


class PassengerAgent(Agent):
    def __init__(self, unique_id, model, demographic):
        super().__init__(unique_id, model)
        self.demographic = demographic
        # Define attributes for the passenger agent based on demographics
        if demographic == "Adult":
            self.preferences = {
                "accessibility": round(np.random.normal(3, 1), 2),
                "leisure_time": round(random.uniform(1, 5), 2)
            }
            self.willingness_to_pay = {
                "base_price": 0.0,    # best price is free
                "max_price": round(np.random.normal(40, 4), 2),
                "price_sensitivity": round(random.uniform(1, 5), 2)
            }
            self.value_perception = {
                "expected_satisfaction": round(random.uniform(1, 5), 2),
                "word_of_mouth": round(random.uniform(1, 5), 2)
            }

        elif demographic == "Senior":
            self.preferences = {
                "accessibility": round(np.random.normal(3, 1), 2),
                "leisure_time": round(random.uniform(1, 5), 2)
            }
            self.willingness_to_pay = {
                "base_price": 0.0,
                "max_price": round(np.random.normal(40, 4), 2),
                "price_sensitivity": round(random.uniform(1, 5), 2)
            }
            self.value_perception = {
                "expected_satisfaction": round(random.uniform(1, 5), 2),
                "word_of_mouth": round(random.uniform(1, 5), 2)
            }

        elif demographic == "Student":
            self.preferences = {
                "accessibility": round(np.random.normal(3, 1), 2),
                "leisure_time": round(random.uniform(1, 5), 2)
            }
            self.willingness_to_pay = {
                "base_price": 0.0,
                "max_price": round(np.random.normal(40, 4), 2),
                "price_sensitivity": round(random.uniform(1, 5), 2)
            }
            self.value_perception = {
                "expected_satisfaction": round(random.uniform(1, 5), 2),
                "word_of_mouth": round(random.uniform(1, 5), 2)
            }

        self.ticket_purchased = False

    def step(self):
      if not self.ticket_purchased:
        utility = self.calculate_utility()

        if utility >= 3.5 and self.willingness_to_pay["base_price"] <= self.model.ticket_price <= self.willingness_to_pay["max_price"]:
            self.ticket_purchased = True


    def determine_weights(self):
        adult_1 = [0.4, 0.15, 0.2, 0.1, 0.15]
        adult_2 = [0.2, 0.15, 0.2, 0.25, 0.2]
        adult_3 = [0.5, 0.05, 0.25, 0.1, 0.1]
        adult_4 = [0.3, 0.2, 0.1, 0.3, 0.1]
        adults = [adult_1, adult_2, adult_3, adult_4]
        senior_1 = [0.1, 0.25, 0.3, 0.15, 0.2]
        senior_2 = [0.2, 0.5, 0.1, 0.1, 0.1]
        senior_3 = [0.25, 0.4, 0.15, 0.15, 0.05]
        senior_4 = [0.2, 0.15, 0.1, 0.3, 0.25]
        seniors = [senior_1, senior_2, senior_3, senior_4]
        student_1 = [0.35, 0.15, 0.1, 0.15, 0.15]
        student_2 = [0.3, 0.2, 0.15, 0.25, 0.05]
        student_3 = [0.2, 0.1, 0.25, 0.2, 0.25]
        student_4 = [0.2, 0.25, 0.1, 0.15, 0.3]
        students = [student_1, student_2, student_3, student_4]
        if self.demographic == "Adult":
            return random.choice(adults)
        elif self.demographic == "Senior":
            return random.choice(seniors)  
        elif self.demographic == "Student":
            return random.choice(students)


    def calculate_utility(self):
        price_difference = self.model.average_competitor_price - self.model.ticket_price
        if price_difference > 0:
            # competitor more expensive, increase utility
            utility_adjustment = 1 + abs(price_difference / self.model.average_competitor_price)
        elif price_difference < 0:
            # yourself more expensive, reduce utility
            utility_adjustment = 1 - abs(price_difference / self.model.ticket_price)
        else:
            utility_adjustment = 1


        features = [
            self.preferences["accessibility"],
            self.preferences["leisure_time"],
            self.willingness_to_pay["price_sensitivity"],
            self.value_perception["expected_satisfaction"],
            self.value_perception["word_of_mouth"] 
        ]

        weights = self.determine_weights()
        base_utility = round(sum(feature * weight for feature, weight in zip(features, weights)), 2)

        # Adjust utility based on the adjustment factor
        utility = round(base_utility  * utility_adjustment, 2)

        return utility
