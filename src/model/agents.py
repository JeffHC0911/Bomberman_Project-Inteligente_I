from mesa import Agent
import random 
from search_algorithms.breadth_first_search import breadth_first_search
from search_algorithms.depth_first_search import depth_first_search
from search_algorithms.uniform_cost_search import uniform_cost_search
from search_algorithms.hill_climbing_search import hill_climbing_search
from search_algorithms.a_start_search import a_star_search
from search_algorithms.beam_search import beam_search

from utils import sort_neighbors

class Bomberman(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.path = []  
        self.algoritmo_ejecutado = False
        self.waiting_for_explosion = False
        self.history = []  
        self.retreat_steps = []
        self.return_path = []  # Añadimos return_path para el regreso
        self.rocks = []  # Lista para guardar las rocas encontradas

    def step(self):
        # Ejecuta el algoritmo de búsqueda solo una vez
        if not self.algoritmo_ejecutado:
            goal_pos = self.find_exit()
            if goal_pos:
                self.path = self.select_algorithm(self.pos, goal_pos)
                if self.path is None:  # Comprobar si path es None
                    self.path = []  # Reiniciar a lista vacía
                self.rocks = [pos for pos in self.path if any(isinstance(agent, Rock) 
                            for agent in self.model.grid.get_cell_list_contents([pos]))]
                if self.path:
                    print(f"Bomberman {self.unique_id} encontró camino: {self.path}")
                    print("Rocas encontradas: ", self.rocks)
                else:
                    print(f"Bomberman {self.unique_id} no encontró camino a la salida")
            else:
                print("No se encontró la salida")
            self.algoritmo_ejecutado = True
            return

        # Comprobar si está esperando la explosión
        self.check_explosion_status()

        # Si hay pasos de retroceso, retrocede
        if self.retreat_steps:
            new_position = self.retreat_steps.pop(0)
            self.return_path.insert(0, self.pos)  # Guarda la posición para el regreso
            self.move(new_position)
            print(f"Retrocedo a {new_position}")
            return

        # Si hay camino de regreso, vuelve al punto de la bomba
        if self.return_path:
            new_position = self.return_path.pop(0)
            self.move(new_position)
            print(f"Regreso a {new_position}")
            return

        # Si no está esperando la explosión y hay un camino
        if not self.waiting_for_explosion and self.path:
            next_position = self.path[0]  # Miramos la siguiente posición

            # Si la siguiente posición es una roca
            if next_position in self.rocks:
                self.place_bomb(next_position)
            else:
                # Guardamos la posición actual en el historial
                self.history.append(self.pos)
                # Avanzamos a la siguiente posición
                new_position = self.path.pop(0)
                self.move(new_position)
                print(f"Avanzo a {new_position}")

            # Verificar si se ha alcanzado la meta
            if next_position == self.find_exit():
                self.model.schedule.remove(self)
                self.model.running = False


    def move(self, next_step):
        self.model.grid.move_agent(self, next_step)
        self.pos = next_step

    def place_bomb(self, next_position):
        # Removemos la roca de la lista de rocas pendientes
        self.rocks.remove(next_position)
        
        # Coloca la bomba en la posición actual
        bomb_agent = Bomb(self.model.schedule.get_agent_count(), self.model, 1, self.pos)
        self.model.schedule.add(bomb_agent)
        self.model.grid.place_agent(bomb_agent, self.pos)
        self.waiting_for_explosion = True
        print(f"Bomba colocada en {self.pos}")

        # Calcula los pasos de retroceso basado en el cooldown
        cooldown_steps = bomb_agent.cooldown
        if len(self.history) >= cooldown_steps:
            self.retreat_steps = self.history[-cooldown_steps:]
            self.retreat_steps.reverse()
            self.history = self.history[:-cooldown_steps]
        else:
            self.retreat_steps = self.history[::-1]
            self.history = []

    def check_explosion_status(self):
        bombs = [agent for agent in self.model.schedule.agents if isinstance(agent, Bomb)]
        explosions = [agent for agent in self.model.schedule.agents if isinstance(agent, Explosion)]
        
        if not bombs and not explosions and self.waiting_for_explosion:
            print("Bomba explotó, comenzando regreso al punto de la bomba.")
            self.waiting_for_explosion = False

    def get_safe_position(self):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Direcciones: arriba, abajo, izquierda, derecha
        for direction in directions:
            adjacent_position = (self.pos[0] + direction[0], self.pos[1] + direction[1])
            if (0 <= adjacent_position[0] < self.model.grid.width) and (0 <= adjacent_position[1] < self.model.grid.height):
                if self.model.grid.is_cell_empty(adjacent_position):
                    return adjacent_position
        return None

    def find_exit(self):
        for agent in self.model.schedule.agents:
            if isinstance(agent, Meta):
                return agent.pos
        return None

    def select_algorithm(self, start, goal):
        neighbors = self.model.grid.get_neighborhood(start, moore=False, include_center=False)
        sort_neighbors(neighbors, start, self.model.priority)
        if self.model.algorithm == "BFS":
            return breadth_first_search(self.model, start, goal, self.model.priority)
        elif self.model.algorithm == "DFS":
            return depth_first_search(self.model, start, goal, self.model.priority)
        elif self.model.algorithm == "UCS":
            return uniform_cost_search(self.model, start, goal, self.model.priority)
        elif self.model.algorithm == "A*":
            return a_star_search(self.model, start, goal, self.model.priority)
        elif self.model.algorithm == "HCS":
            return hill_climbing_search(self.model, start, goal, self.model.priority)
        elif self.model.algorithm == "BS":
            return beam_search(self.model, start, goal, self.model.priority)
        else:
            return []



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
            if not any(isinstance(agent, (Metal, Rock)) for agent in self.model.grid.get_cell_list_contents([pos]))
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

class Explosion(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.cooldown = 1

    def step(self):
        self.cooldown -= 1
        if self.cooldown <= 0:
            print(f"Explosión {self.unique_id} en la posición {self.pos}")
            
            # Obtener todos los agentes en la misma posición
            cell_contents = self.model.grid.get_cell_list_contents([self.pos])
            
            # Crear una lista de agentes a eliminar
            agents_to_remove = []
            for agent in cell_contents:
                if isinstance(agent, Rock):
                    agents_to_remove.append(agent)
            
            # Eliminar los agentes de manera segura
            for agent in agents_to_remove:
                try:
                    print(f"Eliminando Rock {agent.unique_id} en {self.pos}")
                    self.model.grid.remove_agent(agent)
                    self.model.schedule.remove(agent)
                except Exception as e:
                    print(f"Error al eliminar Rock: {e}")
            
            # Eliminar la explosión
            try:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
            except Exception as e:
                print(f"Error al eliminar Explosión: {e}")


class Bomb(Agent):
    def __init__(self, unique_id, model, pd, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.pd = pd
        self.cooldown = pd + 1

    def step(self):
        self.cooldown -= 1
        if self.cooldown <= 0:
            print(f"Bomba {self.unique_id} explotando en {self.pos}")
            
            # Definir área de explosión
            area = self.model.grid.get_neighborhood(
                self.pos, 
                moore=False,  # Solo cruz, no diagonales
                include_center=True,
                radius=1
            )
            
            # Verificar cada posición del área de explosión
            for pos in area:
                if (0 <= pos[0] < self.model.grid.width and 
                    0 <= pos[1] < self.model.grid.height):
                    try:
                        explosion_id = self.model.schedule.get_agent_count() + 1
                        explosion = Explosion(explosion_id, self.model, pos)
                        self.model.grid.place_agent(explosion, pos)
                        self.model.schedule.add(explosion)
                        print(f"Explosión creada en {pos} con ID {explosion_id}")
                    except Exception as e:
                        print(f"Error al crear explosión en {pos}: {e}")
            
            # Eliminar la bomba de manera segura
            try:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
                print(f"Bomba {self.unique_id} eliminada correctamente")
            except Exception as e:
                print(f"Error al eliminar Bomba: {e}")

