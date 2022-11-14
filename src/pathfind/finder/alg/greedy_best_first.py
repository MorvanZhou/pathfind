from pathfind.finder.finder import BaseFinder
from pathfind.finder.frontier import PriorityFrontier
from pathfind.graph.graph import Node


class GreedyBestFirst(BaseFinder):
    def __init__(self, distance="manhattan"):
        super().__init__(PriorityFrontier())
        self.distance_method = distance

    def check_neighbors(self, current: Node):
        for neighbor, cost in self.neighbors(current):
            if neighbor.name not in self.came_from:
                self.frontier.put(neighbor, self.heuristic(neighbor))
                self.came_from[neighbor.name] = current

    def heuristic(self, neighbor) -> float:
        if self.distance_method == "manhattan":
            return self.end.manhattan_distance(neighbor)
        elif self.distance_method == "euclidean":
            return self.end.euclidean_distance(neighbor)
        return self.end.manhattan_distance(neighbor)


class Greedy(GreedyBestFirst):
    pass
