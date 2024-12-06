import numpy as np
from algoritms.PathFinder import PathFinder
from algoritms.AllPaths import AllPaths
from algoritms.Astar import AStar
from itertools import product

class MinMaxBomberman(PathFinder):
    def find_path(self, marcadorTurno, alpha, beta, nivel, bomberman_step, max_level, enemies_positions, is_bomberman, is_chasing):
        
        if bomberman_step == self.goal:
            return 10000, bomberman_step
        
        if bomberman_step in enemies_positions:
            return -10000, bomberman_step

        if nivel == max_level:
            return self.calculate_heuristic(bomberman_step, enemies_positions, is_chasing), bomberman_step

        best_move = None

        if marcadorTurno % 2 == 0:
            evalmax = -np.inf

            possible_steps = self.grid.get_neighborhood(bomberman_step, moore=False, include_center=False)

            for move in possible_steps:
                if self.is_valid_grass_cell(move):
                    val, _ = self.find_path(marcadorTurno + 1, alpha, beta, nivel + 1, move, max_level, enemies_positions, is_bomberman, is_chasing)

                    if val > evalmax:
                        evalmax = val
                        best_move = move
                    alpha = max(alpha, val)
                    if beta <= alpha:
                        break

            return evalmax if best_move else -np.inf, best_move

        else:  
            evalmin = np.inf
            posibles_combinaciones = self.calculate_possible_combinations(enemies_positions)

            if not posibles_combinaciones:
                return evalmin, best_move 
            
            for move in posibles_combinaciones:
                move = list(move)
                val, _ = self.find_path(marcadorTurno + 1, alpha, beta, nivel + 1, bomberman_step, max_level, move, is_bomberman, is_chasing)

                if val < evalmin:
                    evalmin = val
                    best_move = move
                beta = min(beta, val)

                if beta <= alpha:
                    break

            return evalmin if best_move else np.inf, best_move

    def calculate_heuristic(self, bomberman_step, enemies_positions, is_chasing):
        """
        Calcula la heurística combinada para que los enemigos se posicionen estratégicamente
        cerca de la meta y persigan a Bomberman si se acerca.
        """
        distances_to_goal = [
            self.manhattan_distance(enemy, self.goal) for enemy in enemies_positions
        ]

        bomberman_to_goal = self.manhattan_distance(bomberman_step, self.goal)

        distances_to_bomberman = [
            self.manhattan_distance(enemy, bomberman_step) for enemy in enemies_positions
        ]

        # Determinamos si Bomberman está cerca de la meta
        bomberman_close_to_goal_threshold = 80
        bomberman_close_to_goal = bomberman_to_goal <= bomberman_close_to_goal_threshold

        # Determinamos si algún enemigo está lo suficientemente cerca de Bomberman
        enemy_close_to_bomberman_threshold = 10
        enemies_close_to_bomberman = any(
            dist <= enemy_close_to_bomberman_threshold for dist in distances_to_bomberman
        )

        if bomberman_close_to_goal and enemies_close_to_bomberman:
            # Si Bomberman está cerca de la meta y un enemigo está cerca de él, lo persiguen.
            is_chasing = True

        goal_weight = 4.0
        bomberman_weight = 5.0 if bomberman_close_to_goal else 2.0

        heuristic_scores = [
            -goal_weight * dist_to_goal + bomberman_weight * dist_to_bomberman
            for dist_to_goal, dist_to_bomberman in zip(distances_to_goal, distances_to_bomberman)
        ]

        if is_chasing:
            return sum(distances_to_bomberman)  # Minimizar distancia hacia Bomberman
        else:
            return min(heuristic_scores)

    def calculate_possible_combinations(self, enemy_steps, bomberman_step=None, is_chasing=False):
        """
        Calcula todas las combinaciones posibles de movimientos estratégicos
        para que los enemigos consideren tanto el goal como la posición de Bomberman.
        """
        all_possible_steps = []
        
        for enemy_step in enemy_steps:
            neighbors = self.grid.get_neighborhood(enemy_step, moore=False, include_center=False)
            valid_steps = [step for step in neighbors if self.is_accessible_for_enemy(step)]

            if valid_steps:
                if is_chasing and bomberman_step is not None:
                    # Ordenar pasos en función de su proximidad a Bomberman
                    valid_steps = sorted(
                        valid_steps,
                        key=lambda step: self.manhattan_distance(step, bomberman_step)
                    )
                else:
                    # Ordenar pasos en función de su proximidad al goal
                    valid_steps = sorted(
                        valid_steps,
                        key=lambda step: self.manhattan_distance(step, self.goal)
                    )
                all_possible_steps.append(valid_steps)
            else:
                all_possible_steps.append([])

        combinations = list(product(*all_possible_steps))

        # Filtrar combinaciones con enemigos en casillas únicas
        unique_combinations = [
            comb for comb in combinations if len(set(comb)) == len(comb)
        ]

        return unique_combinations
