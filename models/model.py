import mesa
import random
import numpy as np
from mesa import Model
from agents.enemy import enemy as enemyp
from agents.metal import metal
from utils.load import load
from algoritms.MinMaxBomberman import MinMaxBomberman
from algoritms.MinMaxEnemy import MinMaxEnemy
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid

priorities = { 
    "← ↓ ↑ →": ["Izquierda", "Abajo", "Arriba", "Derecha"],
    "→ ↓ ↑ ←": ["Derecha", "Abajo", "Arriba", "Izquierda"],
    "→ ↑ ← ↓": ["Derecha", "Arriba", "Izquierda", "Abajo"],
    "↑ → ← ↓": ["Arriba", "Derecha", "Izquierda", "Abajo"],
    "↓ ↑ → ←": ["Abajo", "Arriba", "Derecha", "Izquierda"],
    "↑ ← ↓ →": ["Arriba", "Izquierda", "Abajo", "Derecha"],
    "↓ ← → ↑": ["Abajo", "Izquierda", "Derecha", "Arriba"],
    "← → ↓ ↑": ["Izquierda", "Derecha", "Abajo", "Arriba"],
    "← ↑ → ↓": ["Izquierda", "Arriba", "Derecha", "Abajo"] 
}

class model(Model):
    def __init__(self, number_of_agents, width, height, map_file, algorithm, priority, heuristic, goal_pos, difficulty):
        self.num_agents = number_of_agents
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.goal = None
        self.map_file = f"maps/{map_file}"
        self.algorithm = algorithm
        self.priority = priorities[priority]
        self.heuristic = heuristic
        self.turn = 0
        self.value = difficulty * 2 + 1 
        self.strategic_pos = []

        load.load_map(self, self.map_file, algorithm, self.priority, heuristic, tuple(goal_pos))
        print("La posición de las rocas es la siguiente: ",self.rocks)

    def step(self) -> None:
        self.schedule.step()
        enemy_positions, enemies = self.get_enemy_positions()

        if self.strategic_pos == []:
            self.strategic_pos = random.sample(list(self.get_valid_positions(self.goal, 4)), len(enemy_positions))
            print(self.strategic_pos)

        if self.algorithm == "MinMax1":
            minmaxb = MinMaxBomberman(self.grid, self.newBombermanAgent.pos, self.goal, self.priority, self.heuristic)
            steps = []

            # Encuentra al enemigo más cercano
            distances = [self.manhattan_distance(enemy.pos, self.newBombermanAgent.pos) for enemy in enemies]
            closest_enemy_idx = np.argmin(distances)

            for idx, enemy in enumerate(enemies):
                if idx == closest_enemy_idx:
                    # El enemigo más cercano persigue a Bomberman
                    target = self.newBombermanAgent.pos
                    chasing = True
                else:
                    # Los demás enemigos van a su posición estratégica asignada
                    target = self.strategic_pos[idx]
                    chasing = False

                minmaxe = MinMaxEnemy(self.grid, enemy.pos, self.goal, self.priority, self.heuristic)
                step = minmaxe.find_path(1, -np.inf, np.inf, 0, enemy.pos, self.newBombermanAgent.pos, self.value, target, chasing)[1]
                steps.append(step)

            _, bomberman_step = minmaxb.find_path(0, -np.inf, np.inf, 0, self.newBombermanAgent.pos, self.value, enemy_positions, True)

            if self.newBombermanAgent in steps and bomberman_step in enemy_positions:
                print("Bomberman ha sido derrotado")
                self.running = False

            for i in range(len(enemies)):
                self.grid.move_agent(enemies[i], steps[i])
            if bomberman_step:
                self.grid.move_agent(self.newBombermanAgent, bomberman_step)
        
        elif self.algorithm == "MinMax2":
            quiet = False
            is_chasing = False
            for enemy in enemies:
                if self.manhattan_distance(self.newBombermanAgent.pos, enemy.pos) <= 10:
                    is_chasing = True
                    quiet = True

            if self.manhattan_distance(self.newBombermanAgent.pos, self.goal) < 80:
                is_chasing = True

            minmaxb = MinMaxBomberman(self.grid, self.newBombermanAgent.pos, self.goal, self.priority, self.heuristic)
            _, steps = minmaxb.find_path(1, -np.inf, np.inf, 0, self.newBombermanAgent.pos, self.value, enemy_positions, True, is_chasing)
            _, bomberman_step = minmaxb.find_path(0, -np.inf, np.inf, 0, self.newBombermanAgent.pos, self.value, enemy_positions, True, is_chasing)

            if self.newBombermanAgent.pos in steps and bomberman_step in enemy_positions:
                print("Bomberman ha sido derrotado")
                self.running = False

            if not quiet:
                pass
            for i in range(len(enemies)):
                self.grid.move_agent(enemies[i], steps[i])

            if bomberman_step:
                self.grid.move_agent(self.newBombermanAgent, bomberman_step)


        
        agents_in_cell = self.grid.get_cell_list_contents(self.newBombermanAgent.pos)
        for a in agents_in_cell:
            if isinstance(a, enemyp):
                print("Bomberman ha sido derrotado")
                self.running = False
        
        if self.newBombermanAgent.pos == self.goal:
            print("Bomberman ha ganado")
            self.running = False     
    
    def get_enemy_positions(self):
        """Obtiene una lista de las posiciones de todos los agentes tipo 'enemy'."""
        enemies = []
        enemy_positions = []
        for agent in self.schedule.agents:
            if isinstance(agent, enemyp):
                enemy_positions.append(agent.pos)
                enemies.append(agent)
        return enemy_positions, enemies
    
    def get_valid_positions(self, start_position, level):
        """
        Obtiene todas las posiciones válidas hasta un nivel dado, 
        expandiendo las posiciones vecinas desde la inicial.

        Args:
            start_position (tuple): Posición inicial (x, y).
            level (int): Número de niveles de expansión.

        Returns:
            set: Conjunto de posiciones válidas (sin repeticiones).
        """
        visited = set()  # Para evitar repetir posiciones
        frontier = {start_position}  # Conjunto de posiciones del nivel actual

        for _ in range(level):
            next_frontier = set()
            for position in frontier:
                neighbors = self.grid.get_neighborhood(position, moore=True, include_center=False)
                for neighbor in neighbors:
                    if neighbor not in visited and self.is_valid_position(neighbor):
                        next_frontier.add(neighbor)
            visited.update(frontier)
            frontier = next_frontier

        return visited

    def is_valid_position(self, position):
        """
        Verifica si una posición es válida (sin agentes 'metal').

        Args:
            position (tuple): Posición a verificar.

        Returns:
            bool: True si la posición es válida, False si no.
        """
        agents_in_cell = self.grid.get_cell_list_contents([position])
        return all(not isinstance(a, metal) for a in agents_in_cell)
    
    def manhattan_distance(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return (abs(x1 - x2) + abs(y1 - y2)) * 10
