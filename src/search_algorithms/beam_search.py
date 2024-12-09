import heapq
from utils import manhattan_distance, euclidean_distance, sort_neighbors

def beam_search(model, start, goal, priority, heuristic, k=2):
    print(f"Inicio de Beam Search: start={start}, goal={goal}, heuristic={heuristic}, ancho del haz k={k}")

    # Selección de la función de heurística
    if heuristic == 'Manhattan':
        heuristic_func = manhattan_distance
    elif heuristic == 'Euclidean':
        heuristic_func = euclidean_distance
    else:
        raise ValueError("Heurística no reconocida")

    # Inicialización
    open_levels = {0: [(start, heuristic_func(goal, start))]}
    visited = set()
    came_from = {start: None}
    g_score = {start: 0}
    exploration_order = -1
    level = 0

    while open_levels:
        # Obtenemos los nodos actuales de este nivel y los ordenamos por heurística y prioridad
        current_level = open_levels.pop(level, [])

        # Si no hay nodos para procesar, avanzamos al siguiente nivel
        if not current_level:
            level += 1
            continue

        # Ordenamos los nodos actuales por la heurística y limitamos al ancho del haz `k`
        current_level.sort(key=lambda x: x[1])
        next_level_candidates = current_level[:k]

        for current, _ in next_level_candidates:
            exploration_order += 1
            model.label_cell(current, exploration_order)
            visited.add(current)

            # Si llegamos al objetivo, reconstruimos el camino
            if current == goal:
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            # Obtener vecinos y ordenarlos según prioridad
            neighbors = model.grid.get_neighborhood(current, moore=False, include_center=False)
            neighbors = sort_neighbors(neighbors, current, priority)

            new_level = []
            for neighbor in neighbors:
                if not model.is_cell_empty(neighbor) or neighbor in visited:
                    continue

                tentative_g_score = g_score[current] + 10

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    came_from[neighbor] = current

                    neighbor_heuristic = heuristic_func(goal, neighbor)
                    new_level.append((neighbor, neighbor_heuristic + tentative_g_score))

            next_level = level + 1
            if next_level in open_levels:
                open_levels[next_level].extend(new_level)
            else:
                open_levels[next_level] = new_level

        level += 1

    print("No se encontró un camino al objetivo.")
    return None
