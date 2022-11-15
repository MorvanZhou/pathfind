from pathfind.finder.finder import BaseFinder
from pathfind.finder.frontier import FifoFrontier
from pathfind.graph.node import Node


class BreadthFirstSearch(BaseFinder):
    def __init__(self):
        super().__init__(FifoFrontier())

    def check_neighbors(self, current: Node):
        for successor in self.successors(current):
            n = successor.node
            if not self.is_discovered(n):
                self.discover(n)
                self.frontier.put(n)
                self.came_from[n.name] = current


class BFS(BreadthFirstSearch):
    pass
