from algoritms.PathFinder import PathFinder

class DFS(PathFinder):
    def find_path(self):
        stack = [self.start]

        while stack:
            current = stack.pop()
            if current == self.goal:
                return self.reconstruct_path(current)

            if current not in self.visited:
                self.visited.add(current)
                #self.label_grass(current)

                possible_steps = self.grid.get_neighborhood(current, moore=False, include_center=False)
                ordered_steps = self.get_ordered_steps(possible_steps, current)

                for next_pos in reversed(ordered_steps):
                    if next_pos not in self.visited and self.is_accessible(next_pos):
                        stack.append(next_pos)
                        self.came_from[next_pos] = current

        return None
