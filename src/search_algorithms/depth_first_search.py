from utils import sort_neighbors

def depth_first_search(model, start, goal, priority):
    print(f"Inicio de DFS: start={start}, goal={goal}")

    stack = [start]  # Pila de posiciones
    visited = set()
    label_counter = 0  # Contador para etiquetas
    path = []  # List to reconstruct the path

    while stack:
        current = stack.pop()

        if current == goal:
            print("¡Meta alcanzada!")
            path.append(current)
            return path  # Retorna el camino cuando se alcanza la meta

        if current not in visited:
            visited.add(current)
            model.label_cell(current, label_counter)
            label_counter += 1
            path.append(current)  # Agrega el nodo al camino actual

            neighbors = model.grid.get_neighborhood(current, moore=False, include_center=False)
            sorted_neighbors = sort_neighbors(neighbors, current, priority)

            print(f"Vecinos de {current}: {sorted_neighbors}")

            for neighbor in reversed(sorted_neighbors):  # Añadimos en orden inverso
                if neighbor not in visited and model.is_cell_empty(neighbor):
                    stack.append(neighbor)
                    print(f"Agregando vecino: {neighbor} a la pila")

    print("No se encontró camino a la meta")
    return None
