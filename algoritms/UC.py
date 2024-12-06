import heapq
from algoritms.PathFinder import PathFinder

class UC(PathFinder):
    def find_path(self):
        queue = [(0, 0, self.start)]
        cost_so_far = {self.start: 0}
        step_counter = 0  # Para controlar el orden de inserción

        while queue:
            current_cost, _, current = heapq.heappop(queue)
            if current == self.goal:
                return self.reconstruct_path(current)

            self.visited.add(current)
            #self.label_grass(current)

            possible_steps = self.grid.get_neighborhood(current, moore=False, include_center=False)
            ordered_steps = self.get_ordered_steps(possible_steps, current)

            for next_pos in ordered_steps:
                new_cost = current_cost + 10
                if next_pos not in self.visited and self.is_accessible(next_pos):
                    if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                        cost_so_far[next_pos] = new_cost
                        step_counter += 1
                        heapq.heappush(queue, (new_cost, step_counter, next_pos))
                        self.came_from[next_pos] = current

        return None
