from collections import deque

def breadth_first_search(model, start, goal):
    print(f"Inicio de BFS: start={start}, goal={goal}")

    queue = deque([[start]])
    visited = set([start])
    
    while queue:
        path = queue.popleft()
        node = path[-1]
        
        print(f"Visitando nodo: {node}, camino hasta ahora: {path}")

        if node == goal:
            print("¡Meta alcanzada!") 
            return path
        
        neighbors = model.grid.get_neighborhood(node, moore=False, include_center=False)
        print(f"Vecinos de {node}: {neighbors}")

        for neighbor in neighbors:
            # Verificar si el vecino es accesible
            is_empty = model.is_cell_empty(neighbor)
            print(f"Verificando vecino: {neighbor}, vacío: {is_empty}")

            if neighbor not in visited and is_empty:
                print(f"Agregando vecino: {neighbor} a la cola")

                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
                visited.add(neighbor)
                print(f"Nuevo camino: {new_path}")

    print("No se encontró camino a la meta")
    return None
