priorities = { 
    "← ↓ ↑ →": ["Izquierda", "Abajo", "Arriba", "Derecha"],
    "→ ↓ ↑ ←": ["Derecha", "Abajo", "Arriba", "Izquierda"],
    "→ ↑ ← ↓": ["Derecha", "Arriba", "Izquierda", "Abajo"],
    "↑ → ← ↓": ["Arriba", "Derecha", "Izquierda", "Abajo"],
    "↓ ↑ → ←": ["Abajo", "Arriba", "Derecha", "Izquierda"],
    "↑ ← ↓ →": ["Arriba", "Izquierda", "Abajo", "Derecha"],
    "↓ ← → ↑": ["Abajo", "Izquierda", "Derecha", "Arriba"],
    "← → ↓ ↑": ["Izquierda", "Derecha", "Abajo", "Arriba"], 
}

def get_priority_index(direction, priority):
    dir_map = {
        (0, 1): "Arriba",  # Ajustado a los nombres en español
        (1, 0): "Derecha",
        (0, -1): "Abajo",
        (-1, 0): "Izquierda"
    }

    dir_name = dir_map.get(direction)
    if dir_name and dir_name in priority:
        return priority.index(dir_name)
    return len(priority)

def sort_neighbors(neighbors, start, priority):
    neighbors_with_directions = [
        (neighbor, (neighbor[0] - start[0], neighbor[1] - start[1])) for neighbor in neighbors
    ]
    
    sorted_neighbors = sorted(neighbors_with_directions, key=lambda x: get_priority_index(x[1], priority))
    return [neighbor for neighbor, direction in sorted_neighbors]

