import heapq
from utils import sort_neighbors

def uniform_cost_search(model, start, goal, priority):
    print(f"Inicio de UCS: start={start}, goal={goal}")

    # Cola de prioridad para almacenar los caminos, ordenada por el costo acumulado
    queue = [(0, [start])]
    visited = set()
    label_counter = 0  # Contador para etiquetas

    while queue:
        cost, path = heapq.heappop(queue)
        node = path[-1]

        print(f"Visitando nodo: {node}, camino hasta ahora: {path}, costo: {cost}")

        if node == goal:
            print("¡Meta alcanzada!")
            return path

        if node in visited:
            continue

        visited.add(node)

        # Etiquetar la celda visitada
        model.label_cell(node, label_counter)
        label_counter += 1

        neighbors = model.grid.get_neighborhood(node, moore=False, include_center=False)
        sorted_neighbors = sort_neighbors(neighbors, node, priority)  # Ordenar vecinos según la prioridad

        print(f"Vecinos de {node}: {sorted_neighbors}")

        for neighbor in sorted_neighbors:
            if neighbor not in visited and model.is_cell_empty(neighbor):
                new_cost = cost + 1  # Suponiendo que cada movimiento tiene un costo de 1
                new_path = list(path)
                new_path.append(neighbor)
                heapq.heappush(queue, (new_cost, new_path))
                print(f"Agregando vecino: {neighbor} a la cola con costo: {new_cost}")

    print("No se encontró camino a la meta")
    return None
