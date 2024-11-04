import heapq
from utils import manhattan_distance, sort_neighbors

def a_star_search(model, start, goal, priority):
    print(f"Inicio de A*: start={start}, goal={goal}")

    # Inicialización
    open_list = []
    visited = set()  # Conjunto de nodos visitados
    g_score = {start: 0}
    f_score = {start: manhattan_distance(goal, start)}
    came_from = {start: None}
    step_counter = 0
    exploration_order = -1  # Contador para el orden de exploración

    # Iniciamos la cola con el nodo inicial
    heapq.heappush(open_list, (f_score[start], step_counter, start))

    while open_list:
        current_f, _, current = heapq.heappop(open_list)

        # Si ya exploramos este nodo, continuamos
        if current in visited:
            continue

        # Marcamos el nodo como visitado y lo etiquetamos
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

        # Obtenemos y ordenamos los vecinos
        neighbors = model.grid.get_neighborhood(current, moore=False, include_center=False)
        sort_neighbors(neighbors, current, priority)

        # Evaluamos cada vecino
        for neighbor in neighbors:
            # Verificamos si el vecino es válido
            if not model.is_cell_empty(neighbor) or neighbor in visited:
                continue

            # Calculamos el nuevo g_score
            tentative_g_score = g_score[current] + 10

            # Si encontramos un mejor camino
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                # Actualizamos los valores para este vecino
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(goal, neighbor)
                
                # Actualizamos el contador de pasos y añadimos a la cola
                step_counter -= 1
                heapq.heappush(open_list, (f_score[neighbor], step_counter, neighbor))

    print("No se encontró un camino al objetivo.")
    return None