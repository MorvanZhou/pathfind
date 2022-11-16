from pathfind.finder.finder import BaseFinder
from pathfind.finder.queue import PriorityFinderQueue
from pathfind.graph.graph import Node


class Dijkstra(BaseFinder):
    def __init__(self):
        super().__init__(PriorityFinderQueue())

    def check_neighbors(self, current: Node):
        for neighbor in self.successors(current):
            n = neighbor.node
            g = self.g(current) + neighbor.weight
            if not self.is_visited(n) or g < self.g(n):
                self.set_g(n, g)
                self.queue.put(n, g)
                self.came_from[n.name] = current
