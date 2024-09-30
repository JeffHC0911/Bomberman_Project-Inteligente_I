from mesa import Agent

class Bomberman(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.power = 1  # Poder de destrucción inicial

    def step(self):
        # Lógica de movimiento y acción de Bomberman
        pass

class Enemy(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Lógica de movimiento y acción del enemigo
        pass

class Rock(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # TODO document why this method is empty
        pass

class Metal(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # TODO document why this method is empty
        pass

class Path(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # TODO document why this method is empty
        pass
