import typing as tp

from pathfind.finder import tool
from pathfind.finder.finder import BaseFinder
from pathfind.finder.queue import PriorityFinderQueue
from pathfind.graph.graph import Node, Grid, Direction


class JumpPointSearch(BaseFinder):
    def __init__(self, distance="manhattan"):
        super().__init__(PriorityFinderQueue())
        self.diagonal_directions = [Direction.NW, Direction.SW, Direction.SE, Direction.NE]
        self.non_diagonal_directions = [Direction.N, Direction.W, Direction.S, Direction.E]
        self.distance_method = distance

    def iter_explore(self, graph: Grid, start: str, end: str):
        if not isinstance(graph, Grid):
            raise TypeError(
                "graph must by Grid. Use pathfind.transform.matrix2graph(map, diagonal=True) to convert your map."
                "Or define your map by using pathfind.Grid()")
        if not graph.has_diagonal:
            raise ValueError("Jump Point Search has to run on a grid with diagonal connections")

        self.start = self.init_start = graph.nodes[start]
        self.end = self.init_end = graph.nodes[end]

        self.queue.put(self.start, self.heuristic(self.start))
        visited = set()

        while not self.queue.empty():
            src_node: Node = self.queue.get()

            # expand src node
            visited.add(src_node.name)
            done = self.explore_non_diagonal(graph, src_node, visited)
            if done:
                return True

            # expand diagonal
            done = self.explore_diagonal(graph, src_node, visited)
            if not done:
                yield None
            else:
                return

    def explore_diagonal(self, graph: Grid, src_node: Node, visited: set) -> bool:
        for d in self.diagonal_directions:
            n = src_node
            while True:
                # scan to each direction
                n = self.scan(graph, n, d, visited)
                if n is self.end:
                    return True
                if n is None:
                    break
                # scan vertically and horizontally
                done = self.explore_non_diagonal(graph, n, visited)
                if done:
                    return True
        return False

    def explore_non_diagonal(self, graph: Grid, src_node: Node, visited: set) -> bool:
        for d in self.non_diagonal_directions:
            n = src_node
            while True:
                n = self.scan(graph, n, d, visited)
                if n is self.end:
                    return True
                if n is None:
                    break
        return False

    def scan(self, graph, n, direction, visited) -> tp.Optional[Node]:
        n_ = graph.get_directed_neighbor(n, direction)
        if n_ is None or n_.name in visited:
            return None
        self.came_from[n_.name] = n
        visited.add(n_.name)
        if graph.has_forced_neighbor(node=n_, direction=direction):
            self.queue.put(n_, self.heuristic(n_))
            return None
        return n_

    def check_neighbors(self, current: Node):
        raise NotImplemented

    def heuristic(self, node: Node) -> float:
        return tool.distance(node, self.end, self.distance_method)


class JPS(JumpPointSearch):
    pass
