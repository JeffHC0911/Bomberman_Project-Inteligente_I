from mesa import Agent
import numpy as np
from algoritms.RandomMove import RandomMove

class enemy(Agent):
    def __init__(self, unique_id, model, priority, search_type, heuristic):
        super().__init__(unique_id, model)
        self.priority = priority
        self.search_type = search_type
        self.heuristic = heuristic
        self.next_step = self.pos
        self.turn = 0
    
    def step(self) -> None:
            
            if self.search_type != "MinMax1" and not self.search_type == "MinMax2":
                step = RandomMove(self.model.grid, self.pos, self.model.goal, self.priority, "")
                step = step.find_path()
                self.model.grid.move_agent(self, step)
            
            # # else:
            # enemy_positions_list = self.model.get_enemy_positions()

            # nenemy = 0
            # for i in range(0, len(enemy_positions_list)):
            #     if enemy_positions_list[i] == self.pos:
            #         nenemy = i

            # minmax = MinMaxEnemy(self.model.grid, self.pos, self.model.goal, self.priority, self.heuristic)
            # _, step = minmax.find_path(1, -np.inf, np.inf, 0, self.pos, self.model.newBombermanAgent.pos, nenemy, False, enemy_positions_list)
            # self.model.grid.move_agent(self, step[nenemy])
            
        