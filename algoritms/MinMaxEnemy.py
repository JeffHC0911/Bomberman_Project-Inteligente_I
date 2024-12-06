import numpy as np
from algoritms.PathFinder import PathFinder
from algoritms.Astar import AStar

class MinMaxEnemy(PathFinder):
    def find_path(self, marcadorTurno, alpha, beta, nivel, enemy_step, bomberman_step, max_level, target, chasing):
        if enemy_step == bomberman_step:
            return -10000, bomberman_step  # Caso de captura

        if nivel == max_level:
            if chasing:
                astar = AStar(self.grid, enemy_step, bomberman_step, self.priority, self.heuristic)
                path = len(astar.find_path("E"))
                valor = -path
                #valor = -self.manhattan_distance(enemy_step, bomberman_step)
            else:
                astar = AStar(self.grid, enemy_step, target, self.priority, self.heuristic)
                path = len(astar.find_path("E"))
                valor = -path
                #valor = -self.manhattan_distance(enemy_step, target)
            return valor, None

        if marcadorTurno % 2 == 0:  # Turno de Bomberman
            evalmax = -np.inf
            best_move = None
            possible_steps = self.grid.get_neighborhood(bomberman_step, moore=False, include_center=False)
            ordered_steps = self.get_ordered_steps(possible_steps, bomberman_step)

            for move in ordered_steps:
                if self.is_accessible_for_enemy(move):
                    val, _ = self.find_path(marcadorTurno + 1, alpha, beta, nivel + 1, enemy_step, move, max_level, target, chasing)
                    if val > evalmax:
                        evalmax = val
                        best_move = move
                    alpha = max(alpha, val)
                    if beta <= alpha:
                        break

            return evalmax, best_move

        else:  # Turno del enemigo
            evalmin = np.inf
            best_move = None
            possible_steps = self.grid.get_neighborhood(enemy_step, moore=False, include_center=False)
            ordered_steps = self.get_ordered_steps(possible_steps, enemy_step)

            for move in ordered_steps:
                if self.is_accessible_for_enemy(move):
                    val, _ = self.find_path(marcadorTurno + 1, alpha, beta, nivel + 1, move, bomberman_step, max_level, target, chasing)
                    if val < evalmin:
                        evalmin = val
                        best_move = move
                    beta = min(beta, val)
                    if beta <= alpha:
                        break

            return evalmin, best_move
