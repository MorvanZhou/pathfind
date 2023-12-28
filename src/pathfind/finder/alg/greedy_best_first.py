from pathfind.finder.finder import BaseFinder
from pathfind.finder.queue import PriorityFinderQueue
from pathfind.finder.tool import DISTANCE_MAP
from pathfind.graph.edge import INFINITY
from pathfind.graph.graph import Node


class GreedyBestFirst(BaseFinder):
    def __init__(self, distance="manhattan"):
        super().__init__(PriorityFinderQueue())
        self.distance_method = DISTANCE_MAP[distance]

    def check_neighbors(self, current: Node):
        for edge in current.edges.values():
            successor = current.successors[edge.id]
            if successor.weight == INFINITY:
                continue
            n = successor.node
            n_name = n.name
            if n_name not in self.came_from:
                self.queue.put(n, self.distance_method(n, self.end))  # priority = heuristic
                self.came_from[n_name] = current


class Greedy(GreedyBestFirst):
    pass
