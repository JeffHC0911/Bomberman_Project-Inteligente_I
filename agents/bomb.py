from mesa import Agent
from agents.explosion import explosion  
from agents.rock import rock
from agents.metal import metal

class bomb(Agent):
    def __init__(self, unique_id, model, pd, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.pd = pd
        self.cooldown = pd + 1

    def step(self):
        self.cooldown -= 1
        if self.cooldown <= 0:
            print(f"Bomba {self.unique_id} explotó en la posición {self.pos}")

            area = self.explosion_area()

            for pos in area:
                if self.model.grid.out_of_bounds(pos):
                    continue
                new_explosion = explosion(self.model.schedule.get_agent_count(), self.model)
                self.model.grid.place_agent(new_explosion, pos)
                self.model.schedule.add(new_explosion)

            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)

    def explosion_area(self):
        """Calcula el área de explosión basada en el poder de destrucción (pd),
        deteniendo la expansión si encuentra un agente roca o metal."""
        explosion_area = [self.pos]

        # Función auxiliar para explorar una dirección
        def explore_direction(dx, dy):
            for step in range(1, self.pd + 1):
                new_pos = (self.pos[0] + step * dx, self.pos[1] + step * dy)
                if self.model.grid.out_of_bounds(new_pos):
                    break
                explosion_area.append(new_pos)

                # Verifica si hay un agente que detenga la explosión
                agents_in_cell = self.model.grid.get_cell_list_contents([new_pos])
                for agent in agents_in_cell:
                    if isinstance(agent, (rock, metal)):
                        return  # Detener la expansión en esta dirección

        # Explorar las cuatro direcciones (arriba, abajo, izquierda, derecha)
        explore_direction(1, 0)   # Derecha
        explore_direction(-1, 0)  # Izquierda
        explore_direction(0, 1)   # Arriba
        explore_direction(0, -1)  # Abajo

        return explosion_area
