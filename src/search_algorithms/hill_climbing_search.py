import math
from utils import sort_neighbors  # Asegúrate de importar correctamente


def heuristic(pos, goal, heuristic_type="manhattan"):
    """Calcula la distancia heurística entre dos posiciones."""
    if heuristic_type == "manhattan":
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
    elif heuristic_type == "euclidean":
        return math.sqrt((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2)
    else:
        raise ValueError("Tipo de heurística no reconocido. Use 'manhattan' o 'euclidean'.")


def hill_climbing_search(model, start, goal, priority, heuristic_type="manhattan"):
    current = start
    visited = set()
    came_from = {start: None}
    path = [start]
    label_counter = 0

    print(f"Inicio de HCS: start={start}, goal={goal}")

    while current != goal:
        visited.add(current)
        model.label_cell(current, label_counter)
        label_counter += 1

        # Obtener los vecinos ordenados de acuerdo a la prioridad
        neighbors = model.grid.get_neighborhood(current, moore=False, include_center=False)
        sorted_neighbors = sort_neighbors(neighbors, current, priority)

        # Filtrar solo los vecinos accesibles
        valid_neighbors = [
            neighbor for neighbor in sorted_neighbors 
            if model.is_cell_empty(neighbor) and neighbor not in visited
        ]

        if not valid_neighbors:
            print("Sin vecinos válidos. No se puede avanzar.")
            return None, list(visited)

        # Seleccionar el vecino con menor valor heurístico
        next_move = min(valid_neighbors, key=lambda pos: heuristic(pos, goal, heuristic_type))

        # Verificar si el próximo movimiento mejora la distancia al objetivo
        if heuristic(next_move, goal, heuristic_type) >= heuristic(current, goal, heuristic_type):
            print("No se encontraron mejores movimientos. Hill climbing terminó.")
            return None, list(visited)

        # Actualizar el diccionario de movimientos
        came_from[next_move] = current
        path.append(next_move)
        current = next_move

    # Reconstruir el camino hacia el objetivo
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]

    return list(reversed(path)), list(visited)
