from mesa import Agent

class ConwayAgent(Agent):
    def __init__(self, model, pos, state = 0):
        """
        Initializes a ConwayAgent (a cell in the grid).
        
        Parameters:
        - model: The model instance the agent belongs to.
        - pos: A tuple (x, y) representing the agent's position on the grid.
        - state: The initial state of the cell (0 = dead, 1 = alive).
        """
        super().__init__(model)
        self.x, self.y = pos
        self.state = None
        self.new_state = None
    def determine_next_state(self):
        """
        Determines the next state of the agent based on Conway's Game of Life rules.
        
        - A live cell with fewer than 2 or more than 3 live neighbors dies.
        - A dead cell with exactly 5 live neighbors becomes alive.
        """
        live_neighbors = sum(neighbor.state for neighbor in self.model.grid.iter_neighbors((self.x, self.y), True))
        if self.state == 1:
            if live_neighbors < 2 or live_neighbors > 3:
                self.new_state = 0
            else: self.new_state = 1
        else:
            if live_neighbors == 5:
                self.new_state = 1
            else:
                self.new_state = 0
    def live_or_die(self):
        """
        Updates the cell's state to the newly determined state.
        """
        self.state = self.new_state
        
