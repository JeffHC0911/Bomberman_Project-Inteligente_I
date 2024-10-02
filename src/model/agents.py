from mesa import Agent

class Bomberman(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        #self.search_algorithm = search_algorithm
        #self.path = []
        #self.direccion_actual = 0
        #self.algoritmo_ejecutado = False

    def step(self):
        self.move()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def find_exit(self):
        """
        Encuentra la posición de la salida en el mapa.
        """
        for agent in self.model.schedule.agents:
            if isinstance(agent, Rock) and agent.is_exit:
                print(f"Salida encontrada en {agent.pos}")
                return agent.pos
        print("No se encontró ninguna roca con salida")
        return None

class Enemy(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Rock(Agent):
    def __init__(self, unique_id, model, is_exit=False):
        super().__init__(unique_id, model)
        self.is_exit = is_exit

    def step(self):
        pass

class Metal(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Path(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass
