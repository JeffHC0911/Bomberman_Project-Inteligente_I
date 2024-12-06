from algoritms.PathFinder import PathFinder

class BeamSearch(PathFinder):
    def find_path(self):
        k = 2
        past_step = None
        visited = []
        dict = {0: [(self.start, 1000)]}
        actual_level = 0
        last_step_used_by_level = {}
        expanded = []
        cost_so_far = {self.start: 0}

        while True:
            new_level = []
            actual_steps = dict[actual_level]

            if actual_steps == []:
                dict.pop(actual_level)
                actual_level = min(dict)
        
            else:
                actual_steps.sort(key=lambda obj: obj[1])
                next_level_steps = actual_steps[:k]

                print("next level steps: ", next_level_steps)
                #for i in next_level_steps:
                    #self.label_grass(i[0])
                for i in next_level_steps:
                    visited.append(i[0])
                    actual_steps.remove(i)

                    neighbors = self.grid.get_neighborhood(i[0], moore=False, include_center=False)
                    neighbors = self.get_ordered_steps(neighbors, i[0])

                    for j in neighbors:
                        if self.is_accessible(j) and j not in visited:
                            cost_so_far[j] = cost_so_far[i[0]] + 10
                            ##print(f"En la casilla {j} ha dado {cost_so_far[j]}")
                            self.came_from[j] = i[0]
                            if self.heuristic == "Manhattan":
                                new_level.append((j, self.manhattan_distance(j, self.goal) + cost_so_far[j]))
                            else:
                                new_level.append((j, self.euclidean_distance(j, self.goal) + cost_so_far[j]))

                        if j == self.goal:
                            print("Se encontró resultado: ")
                            self.came_from[self.start] = None
                            print(self.came_from)
                            for a in visited:
                                print(a)
                        
                            return self.reconstruct_path(j)
                    
                if actual_steps == []:
                    dict.pop(actual_level)
                
                actual_level += 1

                if actual_level not in dict:
                    dict[actual_level] = new_level
                else:
                    dict[actual_level] += new_level
                # self.came_from[selected_step[0]] = past_step
                # past_step = selected_step[0]