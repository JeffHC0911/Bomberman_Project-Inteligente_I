from mesa import Agent

from model.agents.rock import Rock


class Explosion(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.cooldown = 1

    def step(self):
        self.cooldown -= 1
        if self.cooldown <= 0:
            print(f"Explosión {self.unique_id} en la posición {self.pos}")
            
            # Obtener todos los agentes en la misma posición
            cell_contents = self.model.grid.get_cell_list_contents([self.pos])
            
            # Crear una lista de agentes a eliminar
            agents_to_remove = []
            for agent in cell_contents:
                if isinstance(agent, Rock):
                    agents_to_remove.append(agent)
            
            # Eliminar los agentes de manera segura
            for agent in agents_to_remove:
                try:
                    print(f"Eliminando Rock {agent.unique_id} en {self.pos}")
                    self.model.grid.remove_agent(agent)
                    self.model.schedule.remove(agent)
                except Exception as e:
                    print(f"Error al eliminar Rock: {e}")
            
            # Eliminar la explosión
            try:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
            except Exception as e:
                print(f"Error al eliminar Explosión: {e}")