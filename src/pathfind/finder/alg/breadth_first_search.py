from pathfind.finder.finder import BaseFinder
from pathfind.finder.frontier import FIFOFrontier
from pathfind.graph.node import Node


class BreadthFirstSearch(BaseFinder):
    def __init__(self):
        super().__init__(FIFOFrontier())

    def check_neighbors(self, current: Node):
        for neighbor, cost in self.neighbors(current):
            if not self.in_cost_record(neighbor):
                self.reset_cost_to(neighbor, cost)
                self.frontier.put(neighbor)
                self.came_from[neighbor.name] = current


class BFS(BreadthFirstSearch):
    pass
