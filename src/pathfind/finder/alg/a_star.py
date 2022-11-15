from pathfind.finder.alg.greedy_best_first import GreedyBestFirst
from pathfind.graph.graph import Node


class AStar(GreedyBestFirst):
    def __init__(self, k: float = 1.):
        super().__init__()
        if k < 0:
            k = 0
        self.k = k

    def check_neighbors(self, current: Node):
        for neighbor, cost in self.neighbors(current):
            new_cost = self.cost_to(current) + cost
            if not self.is_discovered(neighbor) or new_cost < self.cost_to(neighbor):
                self.discover(neighbor, new_cost)
                priority = new_cost
                if self.k > 0:
                    priority += self.k * self.heuristic(neighbor)
                self.frontier.put(neighbor, priority, new_cost)  # same f = g + h, then sort g
                self.came_from[neighbor.name] = current
