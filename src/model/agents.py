from mesa import Agent
import random 
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
            if goal_pos:
                self.path = self.select_algorithm(self.pos, goal_pos)
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

        # Verificar si se ha alcanzado la meta
        if next_step == self.find_exit():
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
            if isinstance(agent, Meta):
                return agent.pos
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
        # Obtener posiciones posibles para moverse
        possible_moves = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,  
            include_center=False
        )

        # Filtrar las posiciones que no tienen un agente de tipo Metal
        valid_moves = [
            pos for pos in possible_moves 
            if not any(isinstance(agent, Metal) for agent in self.model.grid.get_cell_list_contents([pos]))
        ]
        
         # Elegir una posición aleatoria de las válidas
        if valid_moves:
            new_position = random.choice(valid_moves)
            self.model.grid.move_agent(self, new_position)

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
