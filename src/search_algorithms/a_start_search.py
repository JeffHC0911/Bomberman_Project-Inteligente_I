import heapq
from utils import manhattan_distance, euclidean_distance, sort_neighbors

def a_star_search(model, start, goal, priority, heuristic):
    print(f"Inicio de A*: start={start}, goal={goal}, heuristic={heuristic}")

    # Selección de la función de heurística
    if heuristic == 'Manhattan':
        heuristic_func = manhattan_distance
    elif heuristic == 'Euclidean':
        heuristic_func = euclidean_distance
    else:
        raise ValueError("Heurística no reconocida")

    # Inicialización
    open_list = []
    visited = set()
    g_score = {start: 0}
    f_score = {start: heuristic_func(goal, start)}
    came_from = {start: None}
    step_counter = 0
    exploration_order = -1

    # Iniciamos la cola con el nodo inicial
    heapq.heappush(open_list, (f_score[start], step_counter, start))

    while open_list:
        current_f, _, current = heapq.heappop(open_list)

        if current in visited:
            continue

        exploration_order += 1
        model.label_cell(current, exploration_order)
        visited.add(current)

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        # Obtenemos y ordenamos los vecinos (solo ortogonales, sin diagonales)
        neighbors = model.grid.get_neighborhood(current, moore=False, include_center=False)
        sort_neighbors(neighbors, current, priority)

        for neighbor in neighbors:
            if not model.is_cell_empty(neighbor) or neighbor in visited:
                continue

            # Costo de movimiento constante (10 unidades) para movimientos ortogonales
            tentative_g_score = g_score[current] + 10

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic_func(goal, neighbor)
                
                step_counter -= 1
                heapq.heappush(open_list, (f_score[neighbor], step_counter, neighbor))

    print("No se encontró un camino al objetivo.")
    return None
