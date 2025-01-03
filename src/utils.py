priorities = { 
    "Izq Aba Der Arr": ["Izquierda", "Abajo", "Derecha", "Arriba"],
    "Izq Aba Arr Der": ["Izquierda", "Abajo", "Arriba", "Derecha"],
    "Izq Der Aba Arr": ["Izquierda", "Derecha", "Abajo", "Arriba"],
    "Izq Der Arr Aba": ["Izquierda", "Derecha", "Arriba", "Abajo"],
    "Izq Arr Aba Der": ["Izquierda", "Arriba", "Abajo", "Derecha"],
    "Izq Arr Der Aba": ["Izquierda", "Arriba", "Derecha", "Abajo"],

    "Der Aba Izq Arr": ["Derecha", "Abajo", "Izquierda", "Arriba"],
    "Der Aba Arr Izq": ["Derecha", "Abajo", "Arriba", "Izquierda"],
    "Der Izq Aba Arr": ["Derecha", "Izquierda", "Abajo", "Arriba"],
    "Der Izq Arr Aba": ["Derecha", "Izquierda", "Arriba", "Abajo"],
    "Der Arr Aba Izq": ["Derecha", "Arriba", "Abajo", "Izquierda"],
    "Der Arr Izq Aba": ["Derecha", "Arriba", "Izquierda", "Abajo"],

    "Arr Aba Izq Der": ["Arriba", "Abajo", "Izquierda", "Derecha"],
    "Arr Aba Der Izq": ["Arriba", "Abajo", "Derecha", "Izquierda"],
    "Arr Izq Aba Der": ["Arriba", "Izquierda", "Abajo", "Derecha"],
    "Arr Izq Der Aba": ["Arriba", "Izquierda", "Derecha", "Abajo"],
    "Arr Der Aba Izq": ["Arriba", "Derecha", "Abajo", "Izquierda"],
    "Arr Der Izq Aba": ["Arriba", "Derecha", "Izquierda", "Abajo"],

    "Aba Arr Izq Der": ["Abajo", "Arriba", "Izquierda", "Derecha"],
    "Aba Arr Der Izq": ["Abajo", "Arriba", "Derecha", "Izquierda"],
    "Aba Izq Arr Der": ["Abajo", "Izquierda", "Arriba", "Derecha"],
    "Aba Izq Der Arr": ["Abajo", "Izquierda", "Derecha", "Arriba"],
    "Aba Der Arr Izq": ["Abajo", "Derecha", "Arriba", "Izquierda"],
    "Aba Der Izq Arr": ["Abajo", "Derecha", "Izquierda", "Arriba"],
}


def get_priority_index(direction, priority):
    dir_map = {
        (0, 1): "Arriba",  
        (1, 0): "Derecha",
        (0, -1): "Abajo",
        (-1, 0): "Izquierda"
    }

    dir_name = dir_map.get(direction)
    if dir_name in priority:
        return priority.index(dir_name)
    return -1  # Devuelve -1 si no se encuentra en priority


def sort_neighbors(neighbors, start, priority):
    neighbors_with_directions = [
        (neighbor, (neighbor[0] - start[0], neighbor[1] - start[1])) for neighbor in neighbors
    ]
    
    sorted_neighbors = sorted(neighbors_with_directions, key=lambda x: get_priority_index(x[1], priority))
    return [neighbor for neighbor, direction in sorted_neighbors]

def manhattan_distance(goal, neighbor):
    return (abs(goal[0] - neighbor[0]) + abs(goal[1] - neighbor[1])) * 10

def euclidean_distance(goal, neighbor):
    return (((goal[0] - neighbor[0]) ** 2 + (goal[1] - neighbor[1]) ** 2) ** 0.5) * 10

# Función de heurística de Manhattan
def manhattan_distance_minimax(state):
    goal = state['goal_position']
    current_pos = state['bomberman_position']
    return (abs(goal[0] - current_pos[0]) + abs(goal[1] - current_pos[1])) * 10

# Función de heurística Euclidiana
def euclidean_distance_minimax(state):
    goal = state['goal_position']
    current_pos = state['bomberman_position']
    return ((goal[0] - current_pos[0]) ** 2 + (goal[1] - current_pos[1]) ** 2) ** 0.5

