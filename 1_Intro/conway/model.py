from mesa import Model
from agents import ConwayAgent
from mesa.space import SingleGrid

class ConwayModel(Model):
    def __init__(self, width = 100, height = 100, start_alive = 0.3, seed = None):
        """
        Initializes the ConwayModel, which represents the game grid and agents.

        Parameters:
        - width: The width of the grid (default 100).
        - height: The height of the grid (default 100).
        - start_alive: The probability that a cell starts in the "alive" state (default 30%).
        - seed: Random seed for reproducibility (optional).
        """
        super().__init__(seed=seed)  # Initialize the parent Model class.

        # Create a grid with the given width and height.
        # torus=False ensures that the grid does not wrap around at the edges.
        self.grid = SingleGrid(width, height, torus=False)

        # Iterate over each coordinate in the grid and place a ConwayAgent.
        for cont, (x, y) in self.grid.coord_iter():
            conway = ConwayAgent(self, (x, y))  # Create a new agent at position (x, y).

            # Randomly determine if the cell should start alive or dead.
            if self.random.random() < start_alive:
                conway.state = 1  # Cell starts alive.
            else:
                conway.state = 0  # Cell starts dead.

            self.grid.place_agent(conway, (x, y))  # Place the agent on the grid.

        self.running = True  # Set the model to a running state.

    def step(self):
        """
        Advances the model by one step. 
        - First, all agents determine their next state.
        - Then, all agents update their state accordingly.
        """
        self.agents.do("determine_next_state")  # Execute the state determination function for all agents.
        self.agents.do("live_or_die")  # Apply the state changes to all agents.
