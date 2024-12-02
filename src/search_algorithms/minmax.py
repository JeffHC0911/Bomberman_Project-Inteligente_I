

from search_algorithms.a_start_search import a_star_search


def minimax_with_alpha_beta_and_astar(state, depth, alpha, beta, is_maximizing_player, max_depth, heuristic_func, model, goal):
    """
    Algoritmo Minimax con poda alfa-beta y A* integrado.
    state: el estado actual del juego
    depth: profundidad actual
    alpha: el valor mínimo que el maximizer está dispuesto a aceptar
    beta: el valor máximo que el minimizer está dispuesto a aceptar
    is_maximizing_player: True si es el turno del jugador máximo (enemigo)
    max_depth: profundidad máxima para la búsqueda
    heuristic_func: la función heurística para evaluar los estados
    model: el entorno de juego
    goal: la meta de Bomberman
    """
    
    # Caso base: si alcanzamos la profundidad máxima o el estado es un estado terminal
    if depth == max_depth:
        return heuristic_func(state)  # Evaluamos el estado usando la heurística

    if is_maximizing_player:
        max_eval = float('-inf')
        for child in generate_children_with_astar(state, 'enemy', model, goal):  # Usamos A* para generar hijos del enemigo
            eval = minimax_with_alpha_beta_and_astar(child, depth + 1, alpha, beta, False, max_depth, heuristic_func, model, goal)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Poda
        return max_eval
    else:
        min_eval = float('inf')
        for child in generate_children_with_astar(state, 'bomberman', model, goal):  # Usamos A* para generar hijos de Bomberman
            eval = minimax_with_alpha_beta_and_astar(child, depth + 1, alpha, beta, True, max_depth, heuristic_func, model, goal)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Poda
        return min_eval
    

def generate_children_with_astar(state, player_type, model, goal):
    if goal is None:
        print("Advertencia: el objetivo (goal) no está definido para generar hijos.")
        return []

    children = []
    if player_type == 'enemy':
        enemy_positions = state['enemy_position']
        for enemy_pos in enemy_positions:
            path_to_bomberman = a_star_search(model, enemy_pos, state['bomberman_position'], priority_function='distance', heuristic='Manhattan')
            if path_to_bomberman:
                for move in path_to_bomberman:
                    child_state = state.copy()
                    child_state['enemy_position'] = move
                    children.append(child_state)
    elif player_type == 'bomberman':
        bomberman_pos = state['bomberman_position']
        path_to_goal = a_star_search(model, bomberman_pos, goal, priority_function='distance', heuristic='Manhattan')
        if path_to_goal:
            for move in path_to_goal:
                child_state = state.copy()
                child_state['bomberman_position'] = move
                children.append(child_state)
    return children


