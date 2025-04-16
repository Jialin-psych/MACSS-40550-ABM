from mesa import Agent

class SchellingAgent(Agent):
    ## Initiate agent instance, inherit model trait from parent class
    def __init__(self, model, agent_type, transition_threshold, transition_probability):
        super().__init__(model)
        ## Set agent type
        self.type = agent_type
        # Updated agents so they can switch groups
        ## Time steps needed to change group
        self.transition_threshold = transition_threshold  
        ## Probability to switch group after threshold
        self.transition_probability = transition_probability  
        ## Track time steps surrounded by opposite group
        self.surrounding_opposite_group_count = 0  

    ## Define basic decision rule
    ## The move rule is exactly the same as the original Schelling model
    def move(self):
        ## Get list of neighbors within range of sight
        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore = True, # Moore neighborhood (8 directions)
            include_center = False
        )
        ## Count neighbors of same type as self
        similar_neighbors = len([n for n in neighbors if n.type == self.type])

        ## If unhappy with neighbors (share is less than desired), move to random empty slot
        if (valid_neighbors := len(neighbors)) > 0:
            share_alike = similar_neighbors / valid_neighbors
        else:
            share_alike = 0
        ## If unhappy with neighbors, move to random empty slot. Otherwise add one to model count of happy agents.
        if share_alike < self.model.desired_share_alike:
            self.model.grid.move_to_empty(self)
        else: 
            self.model.happy +=1   

    # Define the switch group rule  
    def switch_group(self):
        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore = True, # Moore neighborhood (8 directions)
            include_center = False
        )
         ## Calculate influence based on proximity (closer neighbors have stronger influence)
        weighted_influence = 0
        total_weight = 0
        for neighbor in neighbors:
            # Get the distance from the agent (closer neighbors get higher influence)
            distance = abs(self.pos[0] - neighbor.pos[0]) + abs(self.pos[1] - neighbor.pos[1])  # Manhattan distance
            weight = 1 / (distance + 1)  # Weight inversely proportional to distance (closer = stronger influence)
            weighted_influence += weight * (1 if neighbor.type == self.type else -1)  # Positive for same group, negative for different group
            total_weight += weight

        # Normalize influence to make sure it's between -1 and 1
        if total_weight > 0:
            weighted_influence /= total_weight
            
        ## Check if agent should switch groups based on neighborhood influence over time
        if self.surrounding_opposite_group_count >= self.transition_threshold:
            if self.random.random() < self.transition_probability:
                # Switch the group
                self.type = 1 - self.type  
                self.surrounding_opposite_group_count = 0  # Reset the count after switching groups
        else:
            # Increase count of time the agent has been surrounded by opposite group
            if weighted_influence < 0:  # More neighbors of the opposite type
                self.surrounding_opposite_group_count += 1
            else:
                self.surrounding_opposite_group_count = 0  # Reset if agent is surrounded by similar group

