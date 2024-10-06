from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

from search_algorithms import breadth_first_search
from .agents import Bomberman, Enemy, Rock, Metal, Path, Meta

class BombermanModel(Model):
    def __init__(self, width, height, num_bombers, num_enemies, algorithm, map_file):
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, torus=False)
        self.algorithm = algorithm
        self.load_and_setup_map(map_file)

        for i in range(num_bombers):
            bomber = Bomberman(i, self)
            self.schedule.add(bomber)
            self.grid.place_agent(bomber, (1, 1))  # Posición inicial, ajustar según el mapa

        for i in range(num_enemies):
            enemy = Enemy(i + num_bombers, self)
            self.schedule.add(enemy)
            self.grid.place_agent(enemy, (width - 2, height - 2))  # Posición inicial, ajustar según el mapa

    def is_cell_empty(self, pos):
        """
        Verifica si la celda en la posición dada está vacía.
        :param pos: Tupla (x, y) de la posición a verificar.
        :return: True si la celda está vacía (sin agentes), False de lo contrario.
        """
        # Obtiene el contenido de la celda en la posición dada
        contents = self.grid.get_cell_list_contents([pos])
        
        # Retorna True si la celda está vacía o solo tiene caminos o la meta
        return all(isinstance(agent, (Path, Meta)) for agent in contents)

    def load_and_setup_map(self, map_file):
        with open(map_file, 'r') as file:
            game_map = [line.strip().split(',') for line in file.readlines()]

        game_map = game_map[::-1]

        for y, row in enumerate(game_map):
            for x, cell in enumerate(row):
                if cell == 'M':
                    metal = Metal((x, y), self)
                    self.grid.place_agent(metal, (x, y))
                elif cell == 'R':
                    rock = Rock((x, y), self)
                    self.grid.place_agent(rock, (x, y))
                elif cell == 'C':
                    path = Path((x, y), self)
                    self.grid.place_agent(path, (x, y))
                elif cell == 'C_b':
                    path = Path((x, y), self)
                    self.grid.place_agent(path, (x, y))
                    bomber = Bomberman((x, y), self)
                    self.schedule.add(bomber)
                    self.grid.place_agent(bomber, (x, y))
                elif cell == 'META':  # Colocar el agente Meta
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


    def step(self):
        self.schedule.step()
