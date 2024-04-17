from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization import Slider

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(sys.path)

#from .model import SkyHelixModel
from model import SkyHelixModel
import math
import numpy as np


def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}

    if agent.ticket_purchased:
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        # portrayal["r"] = 0.2
    return portrayal        

# grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
grid = CanvasGrid(agent_portrayal, 50, 50 , 800, 800)

# grid_width = math.ceil(num_passengers)
server = ModularServer(SkyHelixModel,
                       [grid],
                       "Ticket Purchased Simulation Model",
                       {"num_passengers": Slider("Number of Passengers", value=100, min_value=100, max_value=2500, step=100),
                         "initial_ticket_price": Slider("Initial Ticket Price", value=20, min_value=10, max_value=30, step=5), 
                        "competitors_price":[10, 30, 48, 49.5, 30, 23, 45.5, 12, 40, 42, 34.05, 40, 45.5],
                        "grid_width":50, "grid_height":50}
                        )

server.port = 8521
server.launch()
