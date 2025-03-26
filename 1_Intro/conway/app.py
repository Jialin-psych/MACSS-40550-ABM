import mesa
import numpy as np
from mesa.visualization import SolaraViz, make_space_component

from model import ConwayModel

def agent_portrayal(agent):
    return {
        "color": "red" if agent.state == 0 else "blue",# Dead cells are red, live cells are blue.
        "marker":"s",  # Use a square marker for visualization.
        "size": 40,
    }

# Function to format the appearance of the visualization.
def post_process(ax):
    ax.set_aspect("equal")  # Ensure the aspect ratio is equal (squares remain squares).
    ax.set_xticks([])  # Remove x-axis ticks for a cleaner visualization.
    ax.set_yticks([])  # Remove y-axis ticks for a cleaner visualization.

# Define parameters for the model that can be adjusted in the UI.
model_params = {
    "seed": {
        "type": "InputText",  # UI element to enter a seed value.
        "value": 42,  # Default seed value for random number generation.
        "label": "Random Seed",  # Label for UI display.
    },
    "width": {
        "type": "SliderInt",  # Integer slider to adjust grid width.
        "value": 100,  # Default width.
        "label": "Width",  # Label for UI.
        "min": 5,  # Minimum grid width.
        "max": 100,  # Maximum grid width.
        "step": 1,  # Increment step for the slider.
    },
    "height": {
        "type": "SliderInt",  # Integer slider to adjust grid height.
        "value": 100,  # Default height.
        "label": "Height",  # Label for UI.
        "min": 5,  # Minimum grid height.
        "max": 100,  # Maximum grid height.
        "step": 1,  # Increment step for the slider.
    },
    "start_alive": {
        "type": "SliderFloat",  # Float slider to adjust the fraction of initially alive cells.
        "value": 0.3,  # Default value: 30% of cells start alive.
        "label": "Cells initially alive",  # Label for UI.
        "min": 0,  # Minimum value (0% alive).
        "max": 1,  # Maximum value (100% alive).
        "step": 0.01,  # Step size for the slider (1% increments).
    },
}

# Create an instance of the ConwayModel with default parameters.
conway_model = ConwayModel()

# Create a visualization component for the grid using the agent portrayal function.
SpaceGraph = make_space_component(agent_portrayal, post_process=post_process, draw_grid=False)

# Set up the interactive visualization using SolaraViz.
page = SolaraViz(
    conway_model,  # The Conway's Game of Life model.
    components=[SpaceGraph],  # List of UI components to display (the grid visualization).
    model_params=model_params,  # Pass adjustable model parameters to the UI.
    name="Game of Life",  # Name of the visualization (shown in the UI).
)

# Render the visualization page.
page
