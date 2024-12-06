from collections import deque
from algoritms.PathFinder import PathFinder

class AllPaths(PathFinder):
    def find_path(self):
        # Cola para BFS, cada elemento es una tupla (posicion_actual, ruta_actual)
        queue = deque([(self.start, [self.start])])
        all_paths = []  # Para almacenar todas las rutas encontradas

        while queue:
            current, path = queue.popleft()

            # Si llegamos al objetivo, guardamos la ruta actual
            if current == self.goal:
                all_paths.append(path)
                continue  # No detenemos la búsqueda, seguimos explorando otras rutas

            # Obtener los vecinos de la celda actual
            possible_steps = self.grid.get_neighborhood(current, moore=False, include_center=False)
            ordered_steps = self.get_ordered_steps(possible_steps, current)

            for next_pos in ordered_steps:
                # Usamos 'path' para verificar ciclos en lugar de 'self.visited'
                if next_pos not in path and self.is_valid_grass_cell(next_pos):
                    # Añadir al camino actual y encolar para seguir buscando
                    queue.append((next_pos, path + [next_pos]))

        return all_paths