from pathfind.finder.finder import BaseFinder
from pathfind.finder.frontier import PriorityFrontier
from pathfind.graph.graph import Node


class Dijkstra(BaseFinder):
    def __init__(self):
        super().__init__(PriorityFrontier())

    def check_neighbors(self, current: Node):
        for successor in self.successors(current):
            n = successor.node
            g = self.cost_to(current) + successor.weight
            if not self.is_discovered(n) or g < self.cost_to(n):
                self.discover(n, g)
                self.frontier.put(n, g)
                self.came_from[n.name] = current
