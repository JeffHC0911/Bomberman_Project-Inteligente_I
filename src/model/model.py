from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from .agents import Bomberman, Enemy, Rock, Metal, Path

class BombermanModel(Model):
    def __init__(self, width, height, num_bombers, num_enemies, map_file, heuristic="manhattan"):
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, torus=False)
        self.heuristic = heuristic  # Guardar la heurística seleccionada

        # Cargar y configurar el mapa
        self.load_and_setup_map(map_file)

        # Crear agentes Bomberman
        for i in range(num_bombers):
            bomber = Bomberman(i, self)
            self.schedule.add(bomber)
            self.grid.place_agent(bomber, (1, 1))  # Posición inicial, ajustar según el mapa

        # Crear enemigos
        for i in range(num_enemies):
            enemy = Enemy(i + num_bombers, self)
            self.schedule.add(enemy)
            self.grid.place_agent(enemy, (width - 2, height - 2))  # Posición inicial, ajustar según el mapa

    def load_and_setup_map(self, map_file):
        """
        Carga el mapa desde un archivo de texto y coloca los agentes de entorno en el grid.
        """
        with open(map_file, 'r') as file:
            game_map = [line.strip().split(',') for line in file.readlines()]

        game_map = game_map[::-1]  # Invertir el mapa para que el origen sea abajo a la izquierda

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

    def step(self):
        self.schedule.step()
