from collections import deque
from utils import sort_neighbors  

def breadth_first_search(model, start, goal, priority):
    print(f"Inicio de BFS: start={start}, goal={goal}")

    queue = deque([[start]])
    visited = set([start])
    label_counter = 0  # Contador para etiquetas

    while queue:
        path = queue.popleft()
        node = path[-1]

        print(f"Visitando nodo: {node}, camino hasta ahora: {path}")

        # Etiquetar la celda visitada
        model.label_cell(node, label_counter)
        label_counter += 1

        if node == goal:
            print("¡Meta alcanzada!")
            return path

        neighbors = model.grid.get_neighborhood(node, moore=False, include_center=False)
        sorted_neighbors = sort_neighbors(neighbors, node, priority)  # Ordenar vecinos

        print(f"Vecinos de {node}: {sorted_neighbors}")

        for neighbor in sorted_neighbors:
            if neighbor not in visited and model.is_cell_empty(neighbor):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
                visited.add(neighbor)
                print(f"Agregando vecino: {neighbor} a la cola")

    print("No se encontró camino a la meta")
    return None
