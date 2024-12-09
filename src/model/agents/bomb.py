from mesa import Agent
from model.agents.explosion import Explosion


class Bomb(Agent):
    def __init__(self, unique_id, model, pd, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.pd = pd
        self.cooldown = pd + 1

    def step(self):
        self.cooldown -= 1
        if self.cooldown <= 0:
            print(f"Bomba {self.unique_id} explotando en {self.pos}")
            
            # Definir las direcciones ortogonales
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, abajo, izquierda, derecha
            explosion_area = [self.pos]  # Incluir la posición de la bomba

            # Expandir en cada dirección hasta el alcance `pd`
            for dx, dy in directions:
                for step in range(1, self.pd + 1):
                    new_pos = (self.pos[0] + dx * step, self.pos[1] + dy * step)
                    if (0 <= new_pos[0] < self.model.grid.width and 
                        0 <= new_pos[1] < self.model.grid.height):
                        explosion_area.append(new_pos)

            # Crear explosiones en el área calculada
            for pos in explosion_area:
                if (0 <= pos[0] < self.model.grid.width and 
                    0 <= pos[1] < self.model.grid.height):
                    try:
                        explosion_id = self.model.schedule.get_agent_count() + 1
                        explosion = Explosion(explosion_id, self.model, pos)
                        self.model.grid.place_agent(explosion, pos)
                        self.model.schedule.add(explosion)
                        print(f"Explosión creada en {pos} con ID {explosion_id}")
                    except Exception as e:
                        print(f"Error al crear explosión en {pos}: {e}")
            
            # Eliminar la bomba de manera segura
            try:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
                print(f"Bomba {self.unique_id} eliminada correctamente")
            except Exception as e:
                print(f"Error al eliminar Bomba: {e}")