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

def get_cost(agent):
    """Determina el costo de moverse a una celda en función del tipo de agente."""
    from agents import GrassAgent, RockAgent, MetalAgent, BorderAgent

    if isinstance(agent, GrassAgent):
        return 10
    elif isinstance(agent, (RockAgent, MetalAgent, BorderAgent)):
        return float("inf")
    return 1  # Costo por defecto

def beam_search(model, start, goal, priority, heuristic_type="manhattan", beam_width=4):
    current_pos = start
    path = [start]
    visited = set([start])
    visited_order = [start]
    label_counter = 0

    print(f"Inicio de Beam Search: start={start}, goal={goal}, beam_width={beam_width}")

    # Cola de prioridad inicial
    queue = [(heuristic(start, goal, heuristic_type), start, [start])]

    while queue:
        next_level = []

        # Expansión de nodos según el ancho del haz
        for _ in range(min(beam_width, len(queue))):
            _, current_pos, path_so_far = queue.pop(0)

            # Etiquetado de celdas visitadas en el modelo
            model.label_cell(current_pos, label_counter)
            label_counter += 1

            # Comprobar si alcanzamos el objetivo
            if current_pos == goal:
                return (path_so_far, visited_order)

            # Obtener vecinos ordenados por prioridad
            neighbors = model.grid.get_neighborhood(current_pos, moore=False, include_center=False)
            sorted_neighbors = sort_neighbors(neighbors, current_pos, priority)

            # Filtrar vecinos y calcular costos
            for neighbor in sorted_neighbors:
                if neighbor not in visited:
                    cellmates = model.grid.get_cell_list_contents([neighbor])
                    move_cost = sum(get_cost(agent) for agent in cellmates)

                    if move_cost < float("inf"):
                        h = heuristic(neighbor, goal, heuristic_type)
                        next_level.append((h, neighbor, path_so_far + [neighbor]))
                        visited.add(neighbor)
                        visited_order.append(neighbor)

        # Ordenar el siguiente nivel y limitar el ancho del haz
        next_level.sort(key=lambda x: x[0])
        queue = next_level[:beam_width]

    print("No se encontró un camino hacia el objetivo.")
    return (None, visited_order)  # Retorna una tupla en caso de no encontrar el camino
