import numpy as np
from mesa import Agent
from agents.grass import grass
from agents.bomb import bomb
from agents.rock import rock
from agents.item import item
from agents.explosion import explosion
from algoritms.BFS import BFS
from algoritms.DFS import DFS
from algoritms.UC import UC
from algoritms.Astar import AStar
from algoritms.HillClimbing import HillClimbing
from algoritms.BeamSearch import BeamSearch
from algoritms.Retreat import Retreat

class bomberman(Agent):
    def __init__(self, unique_id, model, search_type, priority, heuristic):
        super().__init__(unique_id, model)
        self.first_move = True
        self.path = []
        self.history = []
        self.full_history = []
        self.search_type = search_type
        self.priority = priority
        self.waiting_for_explosion = False
        self.retreat_steps = []
        self.return_path = []
        self.heuristic = heuristic
        self.pd = 1
        self.wait_time = 0
        self.state = "moving_to_goal"
        self.turn = 0
    
    def step(self) -> None:
        # if self.turn % 2 == 0:
            cell_agents = self.model.grid.get_cell_list_contents([self.pos])
            for agent in cell_agents:
                if isinstance(agent, item):
                    self.pd += 1
                
                    self.model.grid.remove_agent(agent)
                    self.model.schedule.remove(agent)

            if self.pos != self.model.goal and (not self.search_type == "MinMax1" and not self.search_type == "MinMax2"):
                self.move_towards_goal()
            # else:
            #     enemy_positions_list, _ = self.model.get_enemy_positions()
            #     minmax = MinMaxEnemy(self.model.grid, self.pos, self.model.goal, self.priority, self.heuristic)
            #     _, step = minmax.find_path(
            #         marcadorTurno=0,
            #         alpha=-np.inf,
            #         beta=np.inf,
            #         nivel=0,
            #         enemy_step=enemy_positions_list[0],
            #         bomberman_step=self.pos,
            #         nenemy=0,
            #         is_bomberman=True,
            #         enemies_positions=enemy_positions_list
            #     )
            #     if step:
            #         self.model.grid.move_agent(self, step)
            #     else:
            #         self.model.grid.move_agent(self, self.pos)
        # self.turn += 1    

    def move_towards_goal(self) -> None:
        self.check_explosion_status()

        if self.state == "retreating" and self.retreat_steps:
            print("RETREAT: ", self.retreat_steps)
            new_position = self.retreat_steps.pop(0)
            self.return_path.insert(0, self.pos)
            self.full_history.append(self.pos)
            self.model.grid.move_agent(self, new_position)
            print(f"Retrocedo a {new_position}")

            if not self.retreat_steps:
                self.state = "returning"
            return

        if self.state == "returning" and self.return_path and self.waiting_for_explosion == False:
            new_position = self.return_path.pop(0)
            self.full_history.append(self.pos)
            self.model.grid.move_agent(self, new_position)
            print(f"Regreso a {new_position}")

            if not self.return_path:
                self.state = "moving_to_goal"
            return

        if self.state == "moving_to_goal":
            if self.first_move or (self.search_type == "MinMax" and not self.waiting_for_explosion):
                path_finder = self.get_path_finder()
                if path_finder:
                    self.path, _ = path_finder.find_path()
                self.first_move = False

            if self.path:
                next_position = self.path[0]

                cell_agents = self.model.grid.get_cell_list_contents([next_position])
                rock_present = any(isinstance(agent, rock) for agent in cell_agents)

                if rock_present:
                    self.place_bomb(next_position)
                    self.state = "retreating"
                elif not self.waiting_for_explosion:
                    self.history.append(self.pos)
                    self.full_history.append(self.pos)
                    new_position = self.path.pop(0)
                    self.model.grid.move_agent(self, new_position)
                    print(f"Me muevo a {new_position}")
                else:
                    print("Estoy esperando...")
            else:
                self.model.running = False
                print("No hay camino disponible o ya se alcanzó la meta.")

    def place_bomb(self, next_position):
        bomb_agent = bomb(self.model.schedule.get_agent_count(), self.model, self.pd, self.pos)
        self.model.schedule.add(bomb_agent)
        self.model.grid.place_agent(bomb_agent, self.pos)
        self.waiting_for_explosion = True

        safe_retreat = Retreat(
            self.model.grid, self.pos, None, self.priority, self.heuristic,
            bomb_agent.explosion_area()
        )
        safe_path, _ = safe_retreat.find_path()
        print("SAFE PATH: ", safe_path)

        if safe_path:
            self.retreat_steps = safe_path
        else:
            print("No se encontró una casilla segura, retrocediendo por pasos previos.")
            self.retreat_steps = self.full_history[::-1]

    def check_explosion_status(self):
        bombs = [agent for agent in self.model.schedule.agents if isinstance(agent, bomb)]
        explosions = [agent for agent in self.model.schedule.agents if isinstance(agent, explosion)]
        if not bombs and not explosions and self.waiting_for_explosion:
            print("Bomba explotó, comenzando regreso al punto de la bomba.")
            self.waiting_for_explosion = False

    def get_path_finder(self):
        if self.search_type == "BFS":
            return BFS(self.model.grid, self.pos, self.model.goal, self.priority, self.heuristic)
        elif self.search_type == "DFS":
            return DFS(self.model.grid, self.pos, self.model.goal, self.priority, self.heuristic)
        elif self.search_type == "UC":
            return UC(self.model.grid, self.pos, self.model.goal, self.priority, self.heuristic)
        elif self.search_type == "A*" or self.search_type == "MinMax":
            return AStar(self.model.grid, self.pos, self.model.goal, self.priority, self.heuristic)
        elif self.search_type == "Hill Climbing":
            return HillClimbing(self.model.grid, self.pos, self.model.goal, self.priority, self.heuristic)
        elif self.search_type == "Beam Search":
            return BeamSearch(self.model.grid, self.pos, self.model.goal, self.priority, self.heuristic)
        else:
            print("Tipo de búsqueda no válido.")
            return None
