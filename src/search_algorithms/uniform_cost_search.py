import heapq
from utils import sort_neighbors

def uniform_cost_search(model, start, goal, priority):
    queue = [(0, 0, start)]
    visited = set()
    came_from = {start: None}
    cost_so_far = {start: 0} 
    label_counter = 0
    tie_breaker = 0 

    while queue:
        current_cost, _, current = heapq.heappop(queue)

        if current == goal:
            print("¡Meta alcanzada!")
            # Reconstruir el camino
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return list(reversed(path))

        if current in visited:
            continue

        visited.add(current)
        model.label_cell(current, label_counter)
        label_counter += 1

        neighbors = model.grid.get_neighborhood(current, moore=False, include_center=False)
        sorted_neighbors = sort_neighbors(neighbors, current, priority)

        for neighbor in sorted_neighbors:
            if not model.is_cell_empty(neighbor):
                continue

            new_cost = current_cost + 10  # Costo fijo de 10 como especificado

            # Solo agregamos si no hemos visitado o encontramos un camino más corto
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current
                tie_breaker += 1
                heapq.heappush(queue, (new_cost, tie_breaker, neighbor))

    return None