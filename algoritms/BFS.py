from collections import deque
from algoritms.PathFinder import PathFinder

class BFS(PathFinder):
    def find_path(self):
        queue = deque([self.start])

        while queue:
            current = queue.popleft()
            if current == self.goal:
                return self.reconstruct_path(current)

            self.visited.add(current)
            #self.label_grass(current)

            possible_steps = self.grid.get_neighborhood(current, moore=False, include_center=False)
            ordered_steps = self.get_ordered_steps(possible_steps, current)

            for next_pos in ordered_steps:
                if next_pos not in self.visited and next_pos not in queue and self.is_accessible(next_pos):
                    queue.append(next_pos)
                    self.came_from[next_pos] = current

        return None
