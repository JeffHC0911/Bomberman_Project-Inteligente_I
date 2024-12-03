from mesa import Model
import random 
from mesa.time import RandomActivation, SimultaneousActivation
from mesa.space import MultiGrid
import numpy as np
from utils import priorities

from search_algorithms import breadth_first_search
from model.agents.bomberman import Bomberman
from model.agents.enemy import Enemy
from model.agents.rock import Rock
from model.agents.metal import Metal
from model.agents.path import Path
from model.agents.meta import Meta
from model.agents.wildcard import Wildcard
from search_algorithms.minmax import minimax_with_alpha_beta_and_astar


class BombermanModel(Model):
    def __init__(self, width, height, num_bombers, num_enemies, num_wildcards, algorithm, priority, heuristic, map_file, difficulty):
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, torus=False)
        self.algorithm = algorithm
        self.priority = priorities[priority]  # Usar el diccionario de prioridades
        self.heuristic = heuristic
        self.num_wildcards = num_wildcards
        #self.running = True
        self.difficulty = difficulty
        self.bomber = []


        self.load_and_setup_map(map_file)

        for i in range(num_bombers):
            bomber = Bomberman(i, self)
            self.schedule.add(bomber)
            self.grid.place_agent(bomber, (1, 1))  # Posición inicial, ajustar según el mapa
            self.bomber.append(bomber)

        for i in range(num_enemies):
            enemy = Enemy(i + num_bombers, self)
            self.schedule.add(enemy)
            
            # Encuentra una posición inicial válida para el enemigo, que no tenga Metal
            while True:
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                contents = self.grid.get_cell_list_contents((x, y))
                
                # Solo coloca el enemigo si la celda no contiene Metal ni Bomberman
                if not any(isinstance(agent, (Metal, Bomberman, Rock)) for agent in contents):
                    self.grid.place_agent(enemy, (x, y))
                    break

        # Asignar *wildcards* a rocas
        self.assign_wildcards_to_rocks()

    
    def assign_wildcards_to_rocks(self):
        """
        Asocia un número limitado de *wildcards* a rocas seleccionadas al azar.
        """
        # Obtener todas las rocas en el mapa
        rock_agents = [agent for agent in self.schedule.agents if isinstance(agent, Rock)]
        if not rock_agents:
            print("No hay rocas disponibles para asignar *wildcards*.")
            return

        # Seleccionar rocas aleatorias para asignar *wildcards*
        selected_rocks = random.sample(rock_agents, min(self.num_wildcards, len(rock_agents)))

        for rock in selected_rocks:
            wildcard_id = self.schedule.get_agent_count() + 1
            wildcard = Wildcard(wildcard_id, self, rock.pos)
            self.schedule.add(wildcard)  # Solo lo agregamos al schedule, pero no al grid
            rock.comodin_asociado = wildcard  # Vincular el *wildcard* a la roca
            print(f"Wildcard vinculado a la roca en {rock.pos}.")


    def step(self):
        if not self.running:
            return  # Detener si el juego ya no está en ejecución

        # Verificar que Bomberman está creado antes de proceder
        if not self.bomber:
            print("Error: Bomberman no ha sido creado o agregado correctamente.")
            return  # Detener la ejecución si Bomberman no está en la lista

        # Ejecutar los pasos de los agentes (mover a Bomberman y los enemigos)
        self.schedule.step()

        # Obtener las posiciones actuales de los enemigos
        enemy_positions, enemies = self.get_enemy_positions()

        # Obtener la posición de Bomberman y la meta
        bomberman_pos = self.bomber[0].pos  # Suponiendo que sólo hay un Bomberman
        goal_pos = self.goal  # La meta está definida en el modelo

        # Determinar el max_depth en función de la dificultad
        if self.difficulty == 1:
            max_depth = 3  # Baja dificultad
        elif self.difficulty == 2:
            max_depth = 6  # Dificultad media
        else:
            max_depth = 0  # Dificultad 0, no usar Minimax, movimiento aleatorio

        # Ejecutar Minimax con poda alfa-beta solo si la dificultad es 1 o 2
        if self.algorithm == "MinMax" and self.difficulty > 0:
            # Estado de Bomberman y los enemigos
            state = {
                'bomberman_position': bomberman_pos,
                'enemy_position': [enemy.pos for enemy in enemies],
            }

            # Llamar a Minimax para el enemigo (jugadores minimizadores) solo si la dificultad es 1 o 2
            eval_enemy, steps_enemy = minimax_with_alpha_beta_and_astar(
                state, 0, -np.inf, np.inf, False, max_depth,  # Usar max_depth dinámico
                self.heuristic, self, goal_pos
            )

            # Depurar los pasos calculados para los enemigos
            if steps_enemy is not None:
                print(f"Enemy steps calculated: {steps_enemy}")  # Depuración
                # Mover a los enemigos basados en los pasos calculados
                for i, enemy in enumerate(enemies):
                    if i < len(steps_enemy):
                        self.grid.move_agent(enemy, steps_enemy[i])
                        print(f"Enemy {enemy.unique_id} moved to {steps_enemy[i]}")  # Depuración
            else:
                print("Error: No se calculó el camino para los enemigos.")
                return  # Detener ejecución si no se obtienen pasos para los enemigos

            # Llamar a Minimax para Bomberman (jugador maximizador)
            eval_bomberman, bomberman_step = minimax_with_alpha_beta_and_astar(
                state, 0, -np.inf, np.inf, True, max_depth,  # Usar max_depth dinámico
                self.heuristic, self, goal_pos
            )

            # Depurar los pasos de Bomberman
            if bomberman_step:
                print(f"Bomberman steps calculated: {bomberman_step}")  # Depuración
                self.grid.move_agent(self.bomber[0], bomberman_step)
                print(f"Bomberman moved to {bomberman_step}")  # Depuración
            else:
                print("Error: No se calculó el camino para Bomberman.")
                return  # Detener ejecución si no se obtienen pasos para Bomberman

        # Movimiento aleatorio para los enemigos si la dificultad es 0
        elif self.difficulty == 0:

            # Verificar si Bomberman y algún enemigo están en la misma posición
            for cell in self.grid.coord_iter():
                cell_contents = cell[0]
                bomber_present = any(isinstance(agent, Bomberman) for agent in cell_contents)
                enemy_present = any(isinstance(agent, Enemy) for agent in cell_contents)

                if bomber_present and enemy_present:
                    print("Bomberman y Enemy se encontraron. El juego se detiene.")
                    self.running = False  # Detener el juego
                    break

            # Verificar si Bomberman ha llegado a la meta
            if self.bomber[0].pos == self.goal:
                print("Bomberman ha llegado a la meta. El juego se detiene.")
                self.running = False


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
        return all(isinstance(agent, (Path, Meta, Rock, Enemy, Wildcard)) for agent in contents)

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
                    self.bomber.append(bomber)
                elif cell == 'C_m':  # Colocar el agente Meta
                    meta = Meta((x, y), self)
                    self.schedule.add(meta)  # Asegúrate de agregarla al schedule
                    self.grid.place_agent(meta, (x, y))
                    print(f"Meta colocada en {(x, y)}")
                    self.goal = (x, y)

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

    def get_enemy_positions(self):
        """Obtiene una lista de las posiciones de todos los enemigos."""
        enemies = []
        enemy_positions = []
        for agent in self.schedule.agents:
            if isinstance(agent, Enemy):
                enemy_positions.append(agent.pos)
                enemies.append(agent)
        return enemy_positions, enemies

   