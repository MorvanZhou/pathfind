from pathfind.finder.finder import BaseFinder
from pathfind.finder.queue import PriorityFinderQueue
from pathfind.graph.graph import Node


class GreedyBestFirst(BaseFinder):
    def __init__(self, distance="manhattan"):
        super().__init__(PriorityFinderQueue())
        self.distance_method = distance

    def check_neighbors(self, current: Node):
        for neighbor in self.successors(current):
            n = neighbor.node
            if n.name not in self.came_from:
                self.queue.put(n, self.heuristic(n))
                self.came_from[n.name] = current

    def heuristic(self, node: Node) -> float:
        if self.distance_method == "manhattan":
            return self.end.manhattan_distance(node)
        elif self.distance_method == "euclidean":
            return self.end.euclidean_distance(node)
        return self.end.manhattan_distance(node)


class Greedy(GreedyBestFirst):
    pass
