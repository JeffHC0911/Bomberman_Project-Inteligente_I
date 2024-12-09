import random
import numpy as np

from mesa import Agent

from model.agents.metal import Metal
from model.agents.rock import Rock


class Enemy(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Verifica la dificultad y decide si usar Minimax o moverse aleatoriamente
        if self.model.difficulty == 0:
            # Movimiento aleatorio si la dificultad es 0
            self.random_move()
        # Si la dificultad es 1 o 2, el movimiento será gestionado desde el modelo,
        # así que no es necesario hacer nada en el step del enemigo.

    def random_move(self):
        """Movimiento aleatorio del enemigo."""
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
