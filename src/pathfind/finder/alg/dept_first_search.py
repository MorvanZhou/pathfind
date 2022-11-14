from pathfind.finder.finder import BaseFinder
from pathfind.finder.frontier import FILOFrontier
from pathfind.graph.node import Node


class DeptFirstSearch(BaseFinder):
    def __init__(self):
        super().__init__(FILOFrontier())

    def check_neighbors(self, current: Node):
        for neighbor, _ in self.neighbors(current):
            if not self.is_discovered(neighbor):
                self.discover(neighbor)
                self.frontier.put(neighbor)
                self.came_from[neighbor.name] = current


class DFS(DeptFirstSearch):
    pass
