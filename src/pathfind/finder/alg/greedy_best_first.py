from pathfind.finder import tool
from pathfind.finder.finder import BaseFinder
from pathfind.finder.queue import PriorityFinderQueue
from pathfind.graph.edge import INFINITY
from pathfind.graph.graph import Node


class GreedyBestFirst(BaseFinder):
    def __init__(self, distance="manhattan"):
        super().__init__(PriorityFinderQueue())
        self.distance_method = distance

    def check_neighbors(self, current: Node):
        for neighbor in self.successors(current):
            n = neighbor.node
            if neighbor.weight == INFINITY:
                continue
            if n.name not in self.came_from:
                self.queue.put(n, self.heuristic(n))
                self.came_from[n.name] = current

    def heuristic(self, node: Node) -> float:
        return tool.distance(node, self.end, self.distance_method)


class Greedy(GreedyBestFirst):
    pass
