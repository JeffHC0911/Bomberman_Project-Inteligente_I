from mesa import Agent

class grass(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.visited = 0
        self.label = ""