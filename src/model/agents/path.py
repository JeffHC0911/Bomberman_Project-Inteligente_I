from mesa import Agent


class Path(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.label = None  # Inicializa la etiqueta como None
        self.visited = 0  # Inicializa el contador de visitas

    def step(self):
        pass