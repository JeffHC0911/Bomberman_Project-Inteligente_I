import heapq
from utils import manhattan_distance, euclidean_distance, sort_neighbors

def a_star_search(model, start, goal, priority_function, heuristic):
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
    counter = 0  # Usado para resolver empates de prioridad
    heapq.heappush(open_list, (0 + heuristic_func(start, goal), counter, start))  # f = g + h
    came_from = {start: None}
    g_score = {start: 0}  # El costo del camino desde el inicio
    f_score = {start: heuristic_func(start, goal)}  # Estimación del costo total desde inicio hasta el objetivo
    visited = set()
    exploration_order = -1  # Para marcar el orden de exploración

    while open_list:
        # Tomamos el nodo con el menor f_score (y en caso de empate, aplicamos la prioridad proporcionada por el usuario)
        current_f_score, current_counter, current = heapq.heappop(open_list)

        # Marcar la casilla con el orden de exploración
        exploration_order += 1
        model.label_cell(current, exploration_order)

        # Si llegamos al objetivo, reconstruimos el camino
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        visited.add(current)

        # Obtener vecinos y ordenarlos según la prioridad definida por el usuario
        neighbors = model.grid.get_neighborhood(current, moore=False, include_center=False)
        neighbors = sort_neighbors(neighbors, current, priority_function)  # Asegúrate de que la prioridad se aplica aquí

        for neighbor in neighbors:
            if not model.is_cell_empty(neighbor) or neighbor in visited:
                continue

            tentative_g_score = g_score[current] + 10  # Costo de mover a un vecino

            # Si encontramos un mejor camino hacia el vecino, actualizamos los valores
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic_func(neighbor, goal)

                # Añadimos el vecino a la lista abierta con su f_score, prioridad y nodo
                counter += 1  # Asegura que cada nodo tenga una prioridad única
                heapq.heappush(open_list, (f_score[neighbor], counter, neighbor))

    print("No se encontró un camino al objetivo.")
    return None
