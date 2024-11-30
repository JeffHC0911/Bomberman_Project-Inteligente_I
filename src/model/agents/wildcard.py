from mesa import Agent

class Wildcard (Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        

    def step(self):
        pass
       
   