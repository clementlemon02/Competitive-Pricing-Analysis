from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization import Slider
from .model import SkyHelixModel

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}

    if agent.ticket_purchased:
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
    return portrayal        

grid = CanvasGrid(agent_portrayal, 50, 50 , 800, 800)

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
