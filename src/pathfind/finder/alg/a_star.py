from pathfind.finder.alg.greedy_best_first import GreedyBestFirst
from pathfind.graph.graph import Node


class AStar(GreedyBestFirst):
    def __init__(self, k: float = 1.):
        super().__init__()
        if k < 0:
            k = 0
        self.k = k

    def check_neighbors(self, current: Node):
        for successor in self.successors(current):
            n = successor.node
            g = self.cost_to(current) + successor.weight
            if not self.is_discovered(n) or g < self.cost_to(n):
                self.discover(n, g)
                f = g  # priority
                if self.k > 0:
                    f += self.k * self.h(n)
                self.frontier.put(n, f, g)  # same f = g + h, then sort g
                self.came_from[n.name] = current
