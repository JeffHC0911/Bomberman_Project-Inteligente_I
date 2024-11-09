from utils import manhattan_distance, euclidean_distance, sort_neighbors

def hill_climbing_search(model, start, goal, priority, heuristic):
    print(f"Inicio de Hill Climbing: start={start}, goal={goal}, heuristic={heuristic}, priority={priority}")
    
    # Selección de la función de heurística
    if heuristic == 'Manhattan':
        heuristic_func = manhattan_distance
    elif heuristic == 'Euclidean':
        heuristic_func = euclidean_distance
    else:
        raise ValueError("Heurística no reconocida")
    
    current = start
    visited = set([start])
    came_from = {start: None}
    exploration_order = 0
    path_cost = {start: 0}
    
    def get_heuristic_value(pos):
        return heuristic_func(goal, pos) + path_cost[current]
    
    model.label_cell(current, exploration_order)
    current_score = get_heuristic_value(current)
    movement_history = [current]
    levels = [[current]]
    stuck_count = 0

    while current != goal:
        neighbors = model.grid.get_neighborhood(current, moore=False, include_center=False)
        sorted_neighbors = sort_neighbors(neighbors, current, priority)
        valid_neighbors = []

        for neighbor in sorted_neighbors:
            if model.is_cell_empty(neighbor):
                tentative_cost = path_cost[current] + 10
                if neighbor in visited and tentative_cost >= path_cost.get(neighbor, float('inf')):
                    continue
                neighbor_score = heuristic_func(goal, neighbor)
                valid_neighbors.append((neighbor, neighbor_score))

        if not valid_neighbors:
            print(f"No hay vecinos válidos disponibles desde {current}. Retrocediendo.")
            if len(levels) > 1:
                # Retrocede hasta el nodo de menor profundidad que tenga vecinos no explorados
                current = levels[0][0]
                movement_history = [current]  # Restablece el historial
                levels = [[current]]  # Restablece los niveles
                stuck_count += 1
                if stuck_count > 100:
                    print("Búsqueda terminada - no se puede progresar más.")
                    break
                continue
            else:
                print("No se puede encontrar un camino al objetivo.")
                return None

        valid_neighbors.sort(key=lambda x: x[1])
        best_neighbor, best_score = valid_neighbors[0]

        if best_score < current_score or (best_score == current_score and best_neighbor not in visited):
            current = best_neighbor
            current_score = best_score
            visited.add(current)
            came_from[current] = movement_history[-1]
            path_cost[current] = path_cost[came_from[current]] + 10
            movement_history.append(current)
            if len(levels) <= len(movement_history):
                levels.append([])
            levels[len(movement_history) - 1].append(current)
            stuck_count = 0

            exploration_order += 1
            model.label_cell(current, exploration_order)

            if current == goal:
                break
        else:
            for neighbor, score in valid_neighbors:
                if neighbor not in visited:
                    current = neighbor
                    current_score = score
                    visited.add(current)
                    came_from[current] = movement_history[-1]
                    path_cost[current] = path_cost[came_from[current]] + 10

                    movement_history.append(current)
                    if len(levels) <= len(movement_history):
                        levels.append([])
                    levels[len(movement_history) - 1].append(current)
                    exploration_order += 1
                    model.label_cell(current, exploration_order)
                    stuck_count = 0
                    break
            else:
                stuck_count += 1
                if stuck_count > 100:
                    print("Búsqueda terminada - no se puede progresar más.")
                    break

    if current == goal:
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        print("Camino encontrado:", path[::-1])
        return path[::-1]

    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    print("Camino parcial encontrado:", path[::-1])
    return path[::-1]