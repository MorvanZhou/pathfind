from pathfind.finder.finder import BaseFinder
from pathfind.finder.frontier import LifoFrontier
from pathfind.graph.node import Node


class DeptFirstSearch(BaseFinder):
    def __init__(self):
        super().__init__(LifoFrontier())

    def check_neighbors(self, current: Node):
        for successor in self.successors(current):
            n = successor.node
            if not self.is_discovered(n):
                self.discover(n)
                self.frontier.put(n)
                self.came_from[n.name] = current


class DFS(DeptFirstSearch):
    pass
