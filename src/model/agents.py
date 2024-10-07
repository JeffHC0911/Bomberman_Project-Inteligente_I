from mesa import Agent
from search_algorithms.breadth_first_search import breadth_first_search
from search_algorithms.depth_first_search import depth_first_search
from search_algorithms.uniform_cost_search import uniform_cost_search

from utils import sort_neighbors

class Bomberman(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.path = []  # Lista para almacenar el camino encontrado
        self.direccion_actual = 0
        self.algoritmo_ejecutado = False

    def step(self):
        if not self.algoritmo_ejecutado:
            goal_pos = self.find_exit()
            print("goal_pos ", goal_pos)
            if goal_pos:
                print(f"Bomberman {self.unique_id} buscando camino desde {self.pos} a {goal_pos}")
                self.path = self.select_algorithm(self.pos, goal_pos)
                print(f"Camino encontrado: {self.path}")
                if self.path:
                    print(f"Bomberman {self.unique_id} encontró camino: {self.path}")
                else:
                    print(f"Bomberman {self.unique_id} no encontró camino a la salida")
            else:
                print("No se encontró la salida")
            self.algoritmo_ejecutado = True
        
        if self.path and self.direccion_actual < len(self.path):
            next_step = self.path[self.direccion_actual]
            self.move()
            print(f"Bomberman {self.unique_id} moviéndose a {next_step}")

        # Verificar si se ha alcanzado la meta
        if next_step == self.find_exit():
            print("Bomberman ha alcanzado la meta. Deteniendo la simulación.")
            self.model.schedule.remove(self)
            self.model.running = False

    def move(self):
        next_step = self.path[self.direccion_actual]
        self.model.grid.move_agent(self, next_step)
        self.direccion_actual += 1

    def find_exit(self):
        """
        Encuentra la posición de la meta en el mapa.
        """
        for agent in self.model.schedule.agents:
            print(f"Revisando agente: {agent} en posición {agent.pos}, tipo: {type(agent)}")  # Mensaje para depuración
            if isinstance(agent, Meta):
                print(f"Meta encontrada en {agent.pos}")  # Mensaje de depuración
                return agent.pos
        print("No se encontró ninguna meta")  # Mensaje de depuración
        return None
    
    def select_algorithm(self, start, goal):
        # Obtener la lista de vecinos alrededor de la posición actual del agente
        neighbors = self.model.grid.get_neighborhood(start, moore=False, include_center=False)
        
        # Ordenar los vecinos utilizando la función sort_neighbors y la prioridad del modelo
        sort_neighbors(neighbors, start, self.model.priority)

        # Llamar al algoritmo de búsqueda apropiado según lo que ha seleccionado el usuario
        if self.model.algorithm == "BFS":
            return breadth_first_search(self.model, start, goal, self.model.priority)
        elif self.model.algorithm == "DFS":
            return depth_first_search(self.model, start, goal, self.model.priority)
        elif self.model.algorithm == "UCS":
            return uniform_cost_search(self.model, start, goal, self.model.priority)




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
        # Puedes dejar esto vacío o agregar comportamiento en el futuro
        pass

class Meta(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Puedes dejar esto vacío o agregar comportamiento en el futuro
        pass

class Path(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.label = None  # Inicializa la etiqueta como None
        self.visited = 0  # Inicializa el contador de visitas

    def step(self):
        pass
