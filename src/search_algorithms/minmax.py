import numpy as np
from itertools import product
from utils import manhattan_distance, euclidean_distance

def minimax_with_alpha_beta_and_astar(state, depth, alpha, beta, is_maximizing_player, max_depth, heuristic_func, model, goal):
    """
    Algoritmo Minimax con poda alfa-beta y A* integrado.
    """
    
    # Convertir la heurística en una función si es una cadena
    if isinstance(heuristic_func, str):
        if heuristic_func == 'Manhattan':
            heuristic_func = manhattan_distance
        elif heuristic_func == 'Euclidean':
            heuristic_func = euclidean_distance
        else:
            raise ValueError("Heurística no reconocida: " + heuristic_func)

    # Caso base: si alcanzamos la profundidad máxima o el estado es un estado terminal
    if depth == max_depth:
        # Evaluamos el estado usando la heurística (ahora pasando ambos parámetros)
        evaluation = heuristic_func(state, goal)  # Pasar el estado y la meta
        return evaluation, state  # Devolver tanto la evaluación como el estado

    if is_maximizing_player:
        max_eval = -np.inf  # Usar np.inf para infinito negativo
        best_state = state  # Inicializamos el estado mejor encontrado

        # Evaluación de Bomberman (maximizador)
        eval_bomberman, best_state = find_path_minimax(state, 'bomberman', model, goal, max_depth, alpha, beta, True, heuristic_func)
        max_eval = eval_bomberman

        return max_eval, best_state  # Devolver tanto la evaluación como el estado

    else:
        min_eval = np.inf  # Usar np.inf para infinito positivo
        best_state = state  # Inicializamos el estado mejor encontrado

        # Evaluación de los enemigos (minimizadores)
        eval_enemy, best_state = find_path_minimax(state, 'enemy', model, goal, max_depth, alpha, beta, False, heuristic_func)
        min_eval = eval_enemy

        return min_eval, best_state  # Devolver tanto la evaluación como el estado


def find_path_minimax(state, player_type, model, goal, max_depth, alpha, beta, is_bomberman, heuristic_func):
    """Función común para calcular los movimientos de los jugadores."""
    
    # Extraemos las posiciones de los agentes (Bomberman o enemigos)
    if player_type == 'enemy':
        positions = state['enemy_position']
    else:  # 'bomberman'
        positions = [state['bomberman_position']]
    
    eval_move = -np.inf if is_bomberman else np.inf  # Usar np.inf para las evaluaciones
    best_move = None
    
    # Asegurarse de que las posiciones son tuplas de coordenadas (x, y)
    if not all(isinstance(pos, tuple) and len(pos) == 2 for pos in positions):
        print("Error: Las posiciones deben ser tuplas de coordenadas (x, y).")
        return eval_move, best_move  # Salir si las posiciones no están en el formato correcto
    
    # Generar los posibles movimientos para Bomberman o los enemigos
    possible_moves = model.grid.get_neighborhood(positions[0], moore=False, include_center=False)
    
    for move in possible_moves:
        # Aquí generas el nuevo estado después del movimiento
        new_state = state.copy()
        if player_type == 'enemy':
            new_state['enemy_position'] = move
        else:
            new_state['bomberman_position'] = move
        
        eval, _ = minimax_with_alpha_beta_and_astar(
            new_state, 
            0, 
            alpha, 
            beta, 
            not is_bomberman, 
            max_depth, 
            heuristic_func, 
            model, 
            goal
        )
        
        if is_bomberman:
            if eval > eval_move:
                eval_move = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Poda
        else:
            if eval < eval_move:
                eval_move = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Poda

    return eval_move, best_move

