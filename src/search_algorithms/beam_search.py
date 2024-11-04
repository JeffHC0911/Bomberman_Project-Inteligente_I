import heapq
from utils import manhattan_distance, sort_neighbors

def beam_search(model, start, goal, priority, k=2):
    print(f"Inicio de Beam Search: start={start}, goal={goal}, ancho del haz k={k}")

    # Inicialización
    open_levels = {0: [(start, manhattan_distance(goal, start))]}
    visited = set()  # Conjunto de nodos visitados
    came_from = {start: None}
    g_score = {start: 0}
    exploration_order = -1  # Contador para el orden de exploración
    level = 0

    while open_levels:
        # Obtenemos los nodos actuales de este nivel y los ordenamos por heurística
        current_level = open_levels.pop(level, [])
        
        # Si no hay nodos para procesar, avanzamos al siguiente nivel
        if not current_level:
            level += 1
            continue
        
        # Ordenamos los nodos actuales por la heurística y limitamos al ancho del haz `k`
        current_level.sort(key=lambda x: x[1])
        next_level_candidates = current_level[:k]

        # Marcamos los nodos seleccionados y los procesamos
        for current, _ in next_level_candidates:
            # Etiquetado de exploración y registro como visitado
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

            # Obtener vecinos ordenados por la prioridad
            neighbors = model.grid.get_neighborhood(current, moore=False, include_center=False)
            sort_neighbors(neighbors, current, priority)

            # Agregamos vecinos válidos a la siguiente capa
            new_level = []
            for neighbor in neighbors:
                # Verificamos si el vecino es accesible y no visitado
                if not model.is_cell_empty(neighbor) or neighbor in visited:
                    continue

                # Calculamos el nuevo g_score
                tentative_g_score = g_score[current] + 10

                # Solo añadimos si este es el camino óptimo al vecino
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    came_from[neighbor] = current

                    # Añadir a los candidatos del siguiente nivel con su puntaje
                    heuristic = manhattan_distance(goal, neighbor)
                    new_level.append((neighbor, heuristic + tentative_g_score))

            # Añadimos los nodos del nuevo nivel al diccionario `open_levels`
            next_level = level + 1
            if next_level in open_levels:
                open_levels[next_level].extend(new_level)
            else:
                open_levels[next_level] = new_level

        # Avanzamos al siguiente nivel
        level += 1

    print("No se encontró un camino al objetivo.")
    return None
