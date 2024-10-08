from utils import sort_neighbors

def depth_first_search(model, start, goal, priority):
    print(f"Inicio de DFS: start={start}, goal={goal}")

    stack = [start]  # Pila de posiciones
    came_from = {start: None}  # Para reconstruir el camino
    visited = set()
    label_counter = 0  # Contador para etiquetas

    while stack:
        current = stack.pop()

        print(f"Visitando nodo: {current}")

        if current == goal:
            print("¡Meta alcanzada!")
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        if current not in visited:
            visited.add(current)
            model.label_cell(current, label_counter)
            label_counter += 1

            neighbors = model.grid.get_neighborhood(current, moore=False, include_center=False)
            sorted_neighbors = sort_neighbors(neighbors, current, priority)

            print(f"Vecinos de {current}: {sorted_neighbors}")

            for neighbor in reversed(sorted_neighbors):  # Añadimos en orden inverso
                if neighbor not in visited and model.is_cell_empty(neighbor):
                    # Verificar que el movimiento no es en diagonal
                    if abs(current[0] - neighbor[0]) + abs(current[1] - neighbor[1]) == 1:
                        stack.append(neighbor)
                        came_from[neighbor] = current
                        print(f"Agregando vecino: {neighbor} a la pila")

    print("No se encontró camino a la meta")
    return None
