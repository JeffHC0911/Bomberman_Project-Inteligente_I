from collections import deque

def bfs(model, start, goal):
    # Cola para almacenar los nodos a visitar
    queue = deque([[start]])
    # Conjunto para almacenar los nodos visitados
    visited = set([start])
    
    while queue:
        # Obtener el camino actual
        path = queue.popleft()
        # Obtener el último nodo del camino
        node = path[-1]
        
        # Si hemos llegado al objetivo, devolver el camino
        if node == goal:
            return path
        
        # Explorar los vecinos del nodo actual
        for neighbor in model.grid.get_neighborhood(node, moore=False, include_center=False):
            if neighbor not in visited and model.grid.is_cell_empty(neighbor):
                # Crear un nuevo camino añadiendo el vecino
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
                # Marcar el vecino como visitado
                visited.add(neighbor)
    
    # Si no se encuentra un camino, devolver None
    return None
