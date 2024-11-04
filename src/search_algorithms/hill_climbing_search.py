import math
from utils import sort_neighbors

def heuristic(pos, goal, heuristic_type="manhattan"):
    """Calcula la distancia heurística entre dos posiciones."""
    if heuristic_type == "manhattan":
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
    elif heuristic_type == "euclidean":
        return math.sqrt((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2)
    else:
        raise ValueError("Tipo de heurística no reconocido. Use 'manhattan' o 'euclidean'.")

def hill_climbing_search(model, start, goal, priority, heuristic_type="manhattan"):
    current_pos = start
    path = [start]  # Mantiene el camino recorrido
    visited = set([start])  # Almacena los nodos visitados para evitar revisitas
    label_counter = 0

    print(f"Inicio de Hill Climbing: start={start}, goal={goal}")

    while current_pos != goal:
        # Etiquetamos el nodo actual para visualización
        model.label_cell(current_pos, label_counter)
        label_counter += 1

        # Obtener y ordenar los vecinos según prioridad
        neighbors = model.grid.get_neighborhood(current_pos, moore=False, include_center=False)
        sorted_neighbors = sort_neighbors(neighbors, current_pos, priority)

        # Inicializamos variables para encontrar el mejor vecino
        best_neighbor = None
        best_heuristic = float("inf")

        # Buscar el vecino con la mejor heurística
        for neighbor in sorted_neighbors:
            if neighbor not in visited and model.is_cell_empty(neighbor):
                h = heuristic(neighbor, goal, heuristic_type)
                if h < best_heuristic:
                    best_heuristic = h
                    best_neighbor = neighbor

        # Si no hay vecino válido o el mejor vecino no mejora la heurística, termina la búsqueda
        if best_neighbor is None or best_heuristic >= heuristic(current_pos, goal, heuristic_type):
            print("No se encontró un camino directo al objetivo.")
            return None, list(visited)  # Retorna None en caso de no hallar un camino

        # Avanzar al mejor vecino y actualizar estructuras
        current_pos = best_neighbor
        path.append(current_pos)
        visited.add(current_pos)

    return path, list(visited)  # Retorna el camino encontrado y los nodos visitados
