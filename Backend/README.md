## Mesa Simulation Model

The backend utilizes the Mesa framework for agent-based simulation. Mesa is an open-source Python library designed to support the development and analysis of agent-based models.

### Features

- **Agent-Based Modeling**: Mesa provides tools for creating and simulating individual agents with customizable behaviors.
- **Model Design**: With Mesa, you can define the structure of your simulation model, including agents, environment, and schedule.
- **Visualization**: Mesa offers visualization tools to help users understand and analyze the dynamics of agent-based models.

### Implementation

The Mesa simulation model is seamlessly integrated into the `pricesimulation` module of the backend. Within this module, you'll find the `agent.py` file, meticulously defining the behavior and attributes of individual agents participating in the simulation. Complementing this, the `model.py` file serves as the backbone, orchestrating the entire simulation process. It creates the environment, initializes agents, and schedules their interactions. Additionally, `main.py` acts as the primary entry point, where users can effortlessly configure parameters and kick-start the simulation process with ease.

Reference:
- [Mesa Simulation Model](CITATION.bib)
