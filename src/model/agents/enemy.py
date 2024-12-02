import random
import numpy as np

from mesa import Agent

from model.agents.metal import Metal
from model.agents.rock import Rock
from search_algorithms.minmax import minimax_with_alpha_beta_and_astar


class Enemy(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):

        if self.model.algorithm == 'MiniMax':
            # Usar Minimax si la dificultad es mayor a 0
            if self.model.difficulty > 0:
                max_depth = 3 if self.model.difficulty == 1 else 6  # Profundidad según la dificultad

                # Estado inicial para Minimax
                state = {
                    'bomberman_position': self.model.bomber[0].pos if self.model.bomber else None,
                    'enemy_position': [enemy.pos for enemy in self.model.schedule.agents if isinstance(enemy, Enemy)]
                }

                # Ejecutar Minimax con poda alfa-beta
                eval_enemy = minimax_with_alpha_beta_and_astar(
                    state, 0, -np.inf, np.inf, True, max_depth, 
                    self.model.heuristic, self.model, self.model.goal
                )

                # Actualizar posición con el resultado de Minimax
                new_position = eval_enemy['enemy_position'][self.unique_id]
                self.model.grid.move_agent(self, new_position)
                print(f"Enemy {self.unique_id} moves to {new_position} using Minimax")

            else:
                # Movimiento aleatorio para dificultad 0
                self.random_move()
        else:
            # Movimiento aleatorio si no se selecciona Minimax
            self.random_move()
            

    def random_move(self):
        possible_moves = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=False
        )
        valid_moves = [
            pos for pos in possible_moves
            if not any(isinstance(agent, (Metal, Rock)) for agent in self.model.grid.get_cell_list_contents([pos]))
        ]
        if valid_moves:
            new_position = random.choice(valid_moves)
            self.model.grid.move_agent(self, new_position)
            print(f"Enemy {self.unique_id} moves to {new_position} randomly")
