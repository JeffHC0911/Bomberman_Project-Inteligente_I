from mesa import Model
import random 
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from utils import priorities

from search_algorithms import breadth_first_search
from .agents import Bomberman, Enemy, Rock, Metal, Path, Meta

class BombermanModel(Model):
    def __init__(self, width, height, num_bombers, num_enemies, algorithm, priority, heuristic, map_file):
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, torus=False)
        self.algorithm = algorithm
        self.priority = priorities[priority]  # Usar el diccionario de prioridades
        self.heuristic = heuristic
        self.load_and_setup_map(map_file)

        for i in range(num_bombers):
            bomber = Bomberman(i, self)
            self.schedule.add(bomber)
            self.grid.place_agent(bomber, (1, 1))  # Posición inicial, ajustar según el mapa

        for i in range(num_enemies):
            enemy = Enemy(i + num_bombers, self)
            self.schedule.add(enemy)
            
            # Encuentra una posición inicial válida para el enemigo, que no tenga Metal
            while True:
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                contents = self.grid.get_cell_list_contents((x, y))
                
                # Solo coloca el enemigo si la celda no contiene Metal ni Bomberman
                if not any(isinstance(agent, (Metal, Bomberman)) for agent in contents):
                    self.grid.place_agent(enemy, (x, y))
                    break
    
    def step(self):
        if not self.running:
            return  # Detener si el juego ya no está en ejecución
        
        # Ejecutar los pasos de los agentes
        self.schedule.step()
        
        # Verificar si Bomberman y algún enemigo están en la misma posición
        for cell in self.grid.coord_iter():
            cell_contents = cell[0]
            bomber_present = any(isinstance(agent, Bomberman) for agent in cell_contents)
            enemy_present = any(isinstance(agent, Enemy) for agent in cell_contents)
            
            if bomber_present and enemy_present:
                print("Bomberman y Enemy se encontraron. El juego se detiene.")
                self.running = False  # Detener el juego
                break

    def find_empty_cell(self):
        """
        Encuentra una celda vacía aleatoria en el grid.
        :return: Una tupla (x, y) con la posición de una celda vacía.
        """
        empty_cells = [(x, y) for x in range(self.grid.width) for y in range(self.grid.height) if self.is_cell_empty((x, y))]
        return random.choice(empty_cells) if empty_cells else (0, 0)


    def is_cell_empty(self, pos):
        """
        Verifica si la celda en la posición dada está vacía.
        :param pos: Tupla (x, y) de la posición a verificar.
        :return: True si la celda está vacía (sin agentes), False de lo contrario.
        """
        # Obtiene el contenido de la celda en la posición dada
        contents = self.grid.get_cell_list_contents([pos])
        
        # Retorna True si la celda está vacía o solo tiene caminos o la meta
        return all(isinstance(agent, (Path, Meta, Rock)) for agent in contents)

    def load_and_setup_map(self, map_file):
        with open(map_file, 'r') as file:
            game_map = [line.strip().split(',') for line in file.readlines()]

        game_map = game_map[::-1]

        for y, row in enumerate(game_map):
            for x, cell in enumerate(row):
                if cell == 'M':
                    metal = Metal((x, y), self)
                    self.grid.place_agent(metal, (x, y))
                else:
                    # Colocar un camino (Path) en celdas que no contienen Metal
                    path = Path((x, y), self)
                    self.schedule.add(path)
                    self.grid.place_agent(path, (x, y))

                if cell == "R":
                    rock_agent = Rock(self.schedule.get_agent_count(), self)
                    self.schedule.add(rock_agent)
                    self.grid.place_agent(rock_agent, (x, y))
                elif cell == 'C':
                    path = Path((x, y), self)
                    self.grid.place_agent(path, (x, y))
                elif cell == 'C_b':
                    path = Path((x, y), self)
                    self.grid.place_agent(path, (x, y))
                    bomber = Bomberman((x, y), self)
                    self.schedule.add(bomber)
                    self.grid.place_agent(bomber, (x, y))
                elif cell == 'C_m':  # Colocar el agente Meta
                    meta = Meta((x, y), self)
                    self.schedule.add(meta)  # Asegúrate de agregarla al schedule
                    self.grid.place_agent(meta, (x, y))
                    print(f"Meta colocada en {(x, y)}")

                    meta_pos = meta.pos  # Obtener la posición del agente Meta
                    cell_contents = self.grid.get_cell_list_contents([meta_pos])  # Contenido de la celda

                    # Verifica que la celda contenga la meta
                    if any(isinstance(agent, Meta) for agent in cell_contents):
                        print("El agente Meta está en un camino accesible.")
                    else:
                        print("El agente Meta no está en un camino.")

    def label_cell(self, position, label):
        """Etiquetar la celda en la posición dada con un valor."""
        cell_contents = self.grid.get_cell_list_contents([position])
        for agent in cell_contents:
            if isinstance(agent, Path):  # Puedes ajustar esto si utilizas otro tipo para representar caminos
                agent.label = label  # Asigna la etiqueta

