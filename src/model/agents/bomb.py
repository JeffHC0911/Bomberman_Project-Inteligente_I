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
            
            # Definir área de explosión
            area = self.model.grid.get_neighborhood(
                self.pos, 
                moore=False,  # Solo cruz, no diagonales
                include_center=True,
                radius=1
            )
            
            # Verificar cada posición del área de explosión
            for pos in area:
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