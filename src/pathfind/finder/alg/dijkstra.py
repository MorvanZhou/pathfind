from pathfind.finder.finder import BaseFinder
from pathfind.finder.queue import PriorityFinderQueue
from pathfind.graph.graph import Node, INFINITY


class Dijkstra(BaseFinder):
    def __init__(self):
        super().__init__(PriorityFinderQueue())

    def check_neighbors(self, current: Node):
        for edge in current.edges.values():
            successor = current.successors[edge.id]
            if successor.weight == INFINITY:
                continue
            g = self._g[current.name] + successor.weight
            n = successor.node

            # not visited or new g is smaller
            n_name = n.name
            if n_name not in self._g or g < self._g[n_name]:
                self._g[n_name] = g  # set g
                self.queue.put(n, g)
                self.came_from[n_name] = current
