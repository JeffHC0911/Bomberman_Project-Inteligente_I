from mesa import Agent
from agents.rock import rock
from agents.enemy import enemy

class explosion(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cooldown = 1
    
    def step(self):
        self.cooldown -= 1
        if self.cooldown <= 0:
            print(f"Explosión {self.unique_id} explotó en la posición {self.pos}")

            agents_in_same_pos = self.model.grid.get_cell_list_contents([self.pos])

            for agent in agents_in_same_pos:
                if isinstance(agent, rock) or isinstance(agent, enemy):
                    print(f"Agente rock {agent.unique_id} eliminado por la explosión")
                    self.model.grid.remove_agent(agent)
                    self.model.schedule.remove(agent)

            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
