from agents.bomberman import bomberman
from agents.salida import salida
from agents.metal import metal
from agents.grass import grass
from agents.rock import rock
from agents.enemy import enemy
from agents.item import item
import random

class load:
    def load_map(self, map_file, algorithm, priority, heuristic, goal_pos):
        with open(map_file, "r") as f:
            lines = f.readlines()
            lines = lines[::-1]  # Invertir las líneas para darle vuelta al mapa verticalmente
            self.rocks = []
            goal_found = False
            
            print("La posición de meta elegida es: ", goal_pos)
            for y, line in enumerate(lines):
                line = line.strip().split(",")  
                for x, cell in enumerate(line):
                    if cell == "M":
                        wall_agent = metal(self.schedule.get_agent_count(), self)
                        self.schedule.add(wall_agent)
                        self.grid.place_agent(wall_agent, (x, y))
                    else:
                        grass_agent = grass(self.schedule.get_agent_count(), self)
                        self.schedule.add(grass_agent)
                        self.grid.place_agent(grass_agent, (x, y))
                        
                    if cell == "B":
                        bomberman_agent = bomberman(self.schedule.get_agent_count(), self, algorithm, priority, heuristic)
                        self.schedule.add(bomberman_agent)
                        self.grid.place_agent(bomberman_agent, (x, y))
                        self.newBombermanAgent = bomberman_agent
                    elif cell == "E":
                        enemy_agent = enemy(self.schedule.get_agent_count(), self, priority, algorithm, heuristic)
                        self.schedule.add(enemy_agent)
                        self.grid.place_agent(enemy_agent, (x,y))
                    elif cell == "R":
                        rock_agent = rock(self.schedule.get_agent_count(), self)
                        self.schedule.add(rock_agent)
                        self.grid.place_agent(rock_agent, (x,y))
                        self.rocks.append((x,y))

                        if goal_pos == (x,y):
                            print(f"Entro en {(x,y)} con goal_pos {goal_pos}")
                            goal_agent = salida(self.schedule.get_agent_count(), self)
                            self.schedule.add(goal_agent)
                            self.grid.place_agent(goal_agent, (x, y))
                            self.goal = (x, y)
                            goal_found = True
                        
                    elif cell == "C_g":
                        goal_agent = salida(self.schedule.get_agent_count(), self)
                        self.schedule.add(goal_agent)
                        self.grid.place_agent(goal_agent, (x, y))
                        self.goal = (x, y)
                        goal_found = True

            if not goal_found and self.rocks:
                goal_position = random.choice(self.rocks)
                goal_agent = salida(self.schedule.get_agent_count(), self)
                self.schedule.add(goal_agent)
                self.grid.place_agent(goal_agent, goal_position)
                self.goal = goal_position
            
            if self.rocks:
                item_position = random.choice(self.rocks)
                item_agent = item(self.schedule.get_agent_count(), self)
                self.schedule.add(item_agent)
                self.grid.place_agent(item_agent, item_position)

    def get_map_dimensions(map_file):
        with open(map_file, "r") as f:
            lines = f.readlines()
            height = len(lines)
            width = len(lines[0].strip().split(",")) if height > 0 else 0
        return width, height
    
    def get_rock_positions(map_file):
        rock_positions = []
        with open(map_file, "r") as f:
            lines = f.readlines()
            lines = lines[::-1]
            for y, line in enumerate(lines):
                line = line.strip().split(",")
                for x, cell in enumerate(line):
                    if cell == "R":
                        rock_positions.append([x, y])

        return rock_positions