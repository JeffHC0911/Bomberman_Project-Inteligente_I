from abc import ABC, abstractmethod
from agents.metal import metal
from agents.grass import grass
from agents.rock import rock
from agents.salida import salida
from agents.item import item

class PathFinder(ABC):
    def __init__(self, grid, start, goal, priority, heuristic):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.priority = priority
        self.came_from = {start: None}
        self.visited = set()
        self.counter = 0
        self.heuristic = heuristic

    @abstractmethod
    def find_path(self):
        pass

    def is_accessible(self, position):
        agents_in_cell = self.grid.get_cell_list_contents([position])
        return all(not isinstance(a, metal) for a in agents_in_cell)
    
    def is_accessible_for_enemy(self, position):
        agents_in_cell = self.grid.get_cell_list_contents([position])
        return all(not isinstance(a, metal) and (not isinstance(a, rock)) for a in agents_in_cell)
    
    def is_valid_grass_cell(self, position):
        if position == self.goal:
            return True
        agents_in_cell = self.grid.get_cell_list_contents([position])
        
        if len(agents_in_cell) == 1:
            return isinstance(agents_in_cell[0], grass)
        
        has_grass = any(isinstance(agent, grass) for agent in agents_in_cell)
        only_rock_or_metal = all(isinstance(agent, (rock, salida, grass, item)) for agent in agents_in_cell)
        
        return has_grass and only_rock_or_metal

    def reconstruct_path(self, current):
        path = []
        rocks = []
        while current is not None:
            agents_in_cell = self.grid.get_cell_list_contents([current])
            for i in agents_in_cell:
                if isinstance(i, rock):
                    rocks.append(current)
            path.append(current)
            current = self.came_from[current]
        path.reverse()
        return path[1:], rocks

    def label_grass(self, position):
        visited = False
        agents_in_cell = self.grid.get_cell_list_contents([position])
        for agent in agents_in_cell:
            if isinstance(agent, rock):
                visited = True
                agent.label = self.counter
            elif isinstance(agent, grass):
                visited = True
                agent.label = self.counter
        
        if visited:
            print(f"{position} - {self.counter}")
            self.counter += 1

    def get_ordered_steps(self, possible_steps, current):
        new_possible_steps = []
        for i in self.priority:
            if i == "Derecha":
                if current[0] < possible_steps[3][0]:
                    new_possible_steps.append(possible_steps[3])
            elif i == "Izquierda":
                if current[0] > possible_steps[0][0]:
                    new_possible_steps.append(possible_steps[0])
            elif i == "Abajo":
                if current[1] > possible_steps[1][1]:
                    new_possible_steps.append(possible_steps[1])
            elif i == "Arriba":
                if current[1] < possible_steps[2][1]:
                    new_possible_steps.append(possible_steps[2])
        return new_possible_steps
    
    def manhattan_distance(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return (abs(x1 - x2) + abs(y1 - y2)) * 10
    
    def euclidean_distance(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return (((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5) * 10
