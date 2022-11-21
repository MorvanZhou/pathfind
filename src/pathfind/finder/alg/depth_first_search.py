from pathfind.finder.finder import BaseFinder
from pathfind.finder.queue import LifoFinderQueue
from pathfind.graph.edge import INFINITY
from pathfind.graph.node import Node


class DepthFirstSearch(BaseFinder):
    def __init__(self):
        super().__init__(LifoFinderQueue())

    def check_neighbors(self, current: Node):
        for neighbor in self.successors(current):
            n = neighbor.node
            if neighbor.weight == INFINITY:
                continue
            if not self.is_visited(n):
                self.set_g(n)
                self.queue.put(n)
                self.came_from[n.name] = current


class DFS(DepthFirstSearch):
    pass
