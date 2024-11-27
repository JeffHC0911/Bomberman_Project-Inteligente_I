import random

from mesa import Agent

from model.agents.metal import Metal
from model.agents.rock import Rock


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