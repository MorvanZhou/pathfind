from pathfind.finder.alg.greedy_best_first import GreedyBestFirst
from pathfind.graph.graph import Node, INFINITY


class AStar(GreedyBestFirst):
    def __init__(self, k: float = 1., distance="manhattan"):
        super().__init__(distance=distance)
        if k < 0:
            k = 0
        self.k = k

    def check_neighbors(self, current: Node):
        successors = current.successors
        for edge in current.edges.values():
            successor = successors[edge.id]
            if successor.weight == INFINITY:
                continue

            g = self._g[current.name] + successor.weight
            n = successor.node
            # not visited or new g is smaller
            n_name = n.name
            if n_name not in self._g or g < self._g[n_name]:
                self._g[n_name] = g  # set g
                f = g  # priority
                if self.k > 0:
                    f += self.k * self.distance_method(n, self.end)
                self.queue.put(n, f, g)  # same f = g + h, then sort g
                self.came_from[n_name] = current
