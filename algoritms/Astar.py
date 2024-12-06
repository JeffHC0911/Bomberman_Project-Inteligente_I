import heapq
from algoritms.PathFinder import PathFinder

class AStar(PathFinder):
    def find_path(self, user = "B"):
        queue = [(0, 0, self.start)]
        cost_so_far = {self.start: 0}
        step_counter = 0

        while queue:
            current_priority, _, current = heapq.heappop(queue)
            if current == self.goal:
                return self.reconstruct_path(current)

            ##if current not in self.visited:
            ##    self.label_grass(current)
            self.visited.add(current)

            possible_steps = self.grid.get_neighborhood(current, moore=False, include_center=False)
            ordered_steps = self.get_ordered_steps(possible_steps, current)
            ##print(f"Posición actual {current}, Pasos: {ordered_steps}")

            for next_pos in reversed(ordered_steps):
                new_cost = cost_so_far[current] + 10
                if user == "B":
                    validation = self.is_valid_grass_cell(next_pos)
                elif user == "E":
                    validation = self.is_accessible_for_enemy(next_pos)
                if next_pos not in self.visited and validation:
                    if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                        cost_so_far[next_pos] = new_cost
                        step_counter -= 1
                        if self.heuristic == "Manhattan":
                            heuristic = self.manhattan_distance(next_pos, self.goal)
                        else:
                            heuristic = self.euclidean_distance(next_pos, self.goal)
                        priority = new_cost + heuristic
                        heapq.heappush(queue, (priority, step_counter, next_pos))
                        ##self.label_grass(next_pos)
                        self.came_from[next_pos] = current
                    
                    ##print(f"Evaluating node {next_pos}, cost: {new_cost}, heuristic: {heuristic}, priority: {priority}")

        return None, None
