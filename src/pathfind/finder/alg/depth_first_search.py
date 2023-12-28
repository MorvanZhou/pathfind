from pathfind.finder.finder import BaseFinder
from pathfind.finder.queue import LifoFinderQueue
from pathfind.graph.edge import INFINITY
from pathfind.graph.node import Node


class DepthFirstSearch(BaseFinder):
    def __init__(self):
        super().__init__(LifoFinderQueue())

    def check_neighbors(self, current: Node):
        successors = current.successors
        for edge in current.edges.values():
            successor = successors[edge.id]
            if successor.weight == INFINITY:
                continue
            n = successor.node
            # if not visited
            n_name = n.name
            if n_name not in self._g:
                self._g[n_name] = -1  # set g to -1 to mark visited
                self.queue.put(n)
                self.came_from[n_name] = current


class DFS(DepthFirstSearch):
    pass
