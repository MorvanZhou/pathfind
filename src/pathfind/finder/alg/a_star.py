from pathfind.finder.alg.greedy_best_first import GreedyBestFirst
from pathfind.graph.graph import Node


class AStar(GreedyBestFirst):
    def __init__(self, k: float = 1., distance="manhattan"):
        super().__init__(distance=distance)
        if k < 0:
            k = 0
        self.k = k

    def check_neighbors(self, current: Node):
        for neighbor in self.successors(current):
            n = neighbor.node
            g = self.g(current) + neighbor.weight
            if not self.is_visited(n) or g < self.g(n):
                self.set_g(n, g)
                f = g  # priority
                if self.k > 0:
                    f += self.k * self.h(n)
                self.queue.put(n, f, g)  # same f = g + h, then sort g
                self.came_from[n.name] = current
