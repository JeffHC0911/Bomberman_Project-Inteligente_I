from mesa import Agent


class Metal(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Puedes dejar esto vacío o agregar comportamiento en el futuro
        pass