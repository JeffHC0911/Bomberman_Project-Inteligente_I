from mesa import Agent


class Rock(Agent):
    def __init__(self, unique_id, model, is_exit=False):
        super().__init__(unique_id, model)
        self.is_exit = is_exit

    def step(self):
        pass