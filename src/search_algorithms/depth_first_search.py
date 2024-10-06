
def depth_first_search(self, start, goal):
        print(f"Inicio de DFS: start={start}, goal={goal}")
        stack = [[start]]
        visited = set([start])

        while stack:
            path = stack.pop()
            node = path[-1]

            if node == goal:
                print("¡Meta alcanzada!")
                return path
            
            neighbors = self.grid.get_neighborhood(node, moore=False, include_center=False)
            for neighbor in neighbors:
                if neighbor not in visited and self.is_cell_empty(neighbor):
                    new_path = list(path)
                    new_path.append(neighbor)
                    stack.append(new_path)
                    visited.add(neighbor)

        print("No se encontró camino a la meta")
        return None