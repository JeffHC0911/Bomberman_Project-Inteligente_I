from algoritms.PathFinder import PathFinder
from collections import deque

class Retreat(PathFinder):
    def __init__(self, grid, start, goal, priority, heuristic, explosion_area):
        super().__init__(grid, start, goal, priority, heuristic)
        self.explosion_area = set(explosion_area)

    def find_path(self):
        queue = deque([self.start])
        self.visited = set([self.start])

        while queue:
            current = queue.popleft()

            if current not in self.explosion_area:
                return self.reconstruct_path(current)

            possible_steps = self.grid.get_neighborhood(current, moore=False, include_center=False)
            ordered_steps = self.get_ordered_steps(possible_steps, current)

            for next_pos in ordered_steps:
                if next_pos not in self.visited and next_pos not in queue and self.is_accessible_for_enemy(next_pos):
                    queue.append(next_pos)
                    self.came_from[next_pos] = current
                    self.visited.add(next_pos)

        return None
