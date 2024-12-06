from mesa import Agent

class rock(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.label = ""