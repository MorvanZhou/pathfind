from pathfind.graph.graph import Node
from pathfind.finder.alg.greedy_best_first import GreedyBestFirst


class AStar(GreedyBestFirst):
    def __init__(self, k: float = 1.):
        super().__init__()
        self.k = k

    def check_neighbors(self, current: Node):
        for neighbor, cost in self.neighbors(current):
            new_cost = self.cost_to(current) + cost
            if not self.in_cost_record(neighbor) or new_cost < self.cost_to(neighbor):
                self.reset_cost_to(neighbor, new_cost)
                priority = new_cost + self.k * self.heuristic(neighbor)
                self.frontier.put(neighbor, priority)
                self.came_from[neighbor.name] = current
