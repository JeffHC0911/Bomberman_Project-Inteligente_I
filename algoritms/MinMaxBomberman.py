import numpy as np
from algoritms.PathFinder import PathFinder
from itertools import product

class MinMaxBomberman(PathFinder):
    def find_path(self, marcador_turno, alpha, beta, nivel, bomberman_step, max_level, enemies_positions, is_bomberman, is_chasing):
        
        if bomberman_step == self.goal:
            return 100, bomberman_step
        
        if bomberman_step in enemies_positions:
            return -100, bomberman_step

        if nivel == max_level:
            return self.calculate_heuristic(bomberman_step, enemies_positions, is_chasing), bomberman_step

        best_move = None

        if marcador_turno % 2 == 0:
            evalmax = -np.inf

            possible_steps = self.grid.get_neighborhood(bomberman_step, moore=False, include_center=False)

            for move in possible_steps:
                if self.is_valid_grass_cell(move):
                    val, _ = self.find_path(marcador_turno + 1, alpha, beta, nivel + 1, move, max_level, enemies_positions, is_bomberman, is_chasing)

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
                val, _ = self.find_path(marcador_turno + 1, alpha, beta, nivel + 1, bomberman_step, max_level, move, is_bomberman, is_chasing)

                if val < evalmin:
                    evalmin = val
                    best_move = move
                beta = min(beta, val)

                if beta <= alpha:
                    break

            return evalmin if best_move else np.inf, best_move

    def calculate_heuristic(self, bomberman_step, enemies_positions, is_chasing):
        """
        Calcula una heurística basada en la zona de peligro (proximidad entre Bomberman y enemigos)
        y la proximidad de los enemigos a la meta.
        """
        bomberman_to_goal = self.manhattan_distance(bomberman_step, self.goal)
        distances_to_bomberman = [
            self.manhattan_distance(enemy, bomberman_step) for enemy in enemies_positions
        ]

        distances_to_goal = [
            self.manhattan_distance(enemy, self.goal) for enemy in enemies_positions
        ]
        
        # Zonas de peligro y cercanía a la meta
        danger_zone_threshold = 5  # Umbral de "peligro" cercano
        goal_influence_threshold = 10  # Umbral para la influencia de la meta

        # Determinamos si algún enemigo está cerca de la zona de peligro
        enemies_in_danger_zone = [
            dist <= danger_zone_threshold for dist in distances_to_bomberman
        ]

        # Influencia de la meta sobre los enemigos
        enemies_close_to_goal = [
            dist <= goal_influence_threshold for dist in distances_to_goal
        ]

        # Calculamos la heurística para el Bomberman
        bomberman_score = 0
        if bomberman_to_goal < goal_influence_threshold:
            bomberman_score += 50  # Bonificación por estar cerca de la meta

        # Penalizamos a los enemigos si están en la zona de peligro de Bomberman
        danger_penalty = sum([1 for in_danger in enemies_in_danger_zone if in_danger]) * -10
        
        # Bonificación por enemigos cerca de la meta
        goal_benefit = sum([1 for close_to_goal in enemies_close_to_goal if close_to_goal]) * 5

        # Heurística final para los enemigos
        heuristic_scores = [
            -self.manhattan_distance(enemy, self.goal) + danger_penalty + goal_benefit
            for enemy in enemies_positions
        ]

        # Si los enemigos están persiguiendo a Bomberman, priorizamos las distancias
        if is_chasing:
            return sum(distances_to_bomberman)  # Minimizar la distancia hacia Bomberman
        else:
            return min(heuristic_scores)  # Elegir el mejor puntaje para los enemigos


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
