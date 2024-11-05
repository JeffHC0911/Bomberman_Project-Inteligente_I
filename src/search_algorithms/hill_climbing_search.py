from utils import manhattan_distance, sort_neighbors

def hill_climbing_search(model, start, goal, priority):
    print(f"Inicio de Hill Climbing: start={start}, goal={goal}")
    
    # Estado inicial
    current = start
    visited = set([start])
    came_from = {start: None}
    exploration_order = 0
    path_cost = {start: 0}  # Añadimos un registro del costo del camino
    
    # Función para calcular el valor heurístico combinado
    def get_heuristic_value(pos):
        return manhattan_distance(goal, pos) + path_cost[current]
    
    # Etiquetar nodo inicial
    model.label_cell(current, exploration_order)
    current_score = get_heuristic_value(current)
    
    # Lista para mantener un historial de movimientos
    movement_history = [current]
    stuck_count = 0  # Contador para detectar cuando estamos atascados
    
    while current != goal:
        # Obtener y ordenar vecinos
        neighbors = model.grid.get_neighborhood(current, moore=False, include_center=False)
        valid_neighbors = []
        
        # Filtrar y evaluar vecinos
        for neighbor in neighbors:
            if model.is_cell_empty(neighbor):
                # Calcular el costo tentativo para llegar a este vecino
                tentative_cost = path_cost[current] + 10  # Costo base por movimiento
                
                # Si el vecino ya fue visitado, solo lo consideramos si encontramos un mejor camino
                if neighbor in visited and tentative_cost >= path_cost.get(neighbor, float('inf')):
                    continue
                
                # Calcular score combinando distancia al objetivo y costo del camino
                neighbor_score = manhattan_distance(goal, neighbor)
                valid_neighbors.append((neighbor, neighbor_score))
        
        if not valid_neighbors:
            print("No hay vecinos válidos disponibles.")
            if current == goal:
                break
            # Intentar retroceder si es posible
            if len(movement_history) > 1:
                current = movement_history[-2]
                movement_history.pop()
                stuck_count += 1
                if stuck_count > 100:  # Evitar bucles infinitos
                    print("Búsqueda terminada - no se puede progresar más.")
                    break
                continue
            else:
                print("No se puede encontrar un camino al objetivo.")
                return None
        
        # Ordenar vecinos por score (menor es mejor)
        valid_neighbors.sort(key=lambda x: x[1])
        best_neighbor, best_score = valid_neighbors[0]
        
        # Verificar si el mejor vecino es mejor que la posición actual
        if best_score < current_score or (best_score == current_score and best_neighbor not in visited):
            # Actualizar posición actual
            current = best_neighbor
            current_score = best_score
            visited.add(current)
            came_from[current] = movement_history[-1]
            path_cost[current] = path_cost[came_from[current]] + 10
            
            # Actualizar historial de movimientos
            movement_history.append(current)
            stuck_count = 0  # Resetear contador de atasco
            
            # Etiquetar exploración
            exploration_order += 1
            model.label_cell(current, exploration_order)
            
            if current == goal:
                break
        else:
            # Si no podemos mejorar, intentamos un movimiento lateral
            for neighbor, score in valid_neighbors:
                if neighbor not in visited:
                    current = neighbor
                    current_score = score
                    visited.add(current)
                    came_from[current] = movement_history[-1]
                    path_cost[current] = path_cost[came_from[current]] + 10
                    
                    movement_history.append(current)
                    
                    exploration_order += 1
                    model.label_cell(current, exploration_order)
                    stuck_count = 0
                    break
            else:
                stuck_count += 1
                if stuck_count > 100:
                    print("Búsqueda terminada - no se puede progresar más.")
                    break
    
    # Reconstruir el camino final
    if current == goal:
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        return path[::-1]
    
    # Si llegamos aquí sin encontrar el objetivo, devolvemos el mejor camino encontrado
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    return path[::-1]