import typing as tp

from pathfind.finder import tool
from pathfind.finder.finder import BaseFinder
from pathfind.finder.queue import PriorityFinderQueue
from pathfind.graph.graph import Node, Grid, Direction


def has_forced_neighbor(grid: Grid, node: Node, direction: Direction) -> bool:
    row, col = grid.node2coord[node.name]
    if direction == Direction.N:
        for delta in [-1, 1]:
            if grid.coord_blocked(row, col + delta) \
                    and not grid.coord_blocked(row - 1, col + delta):
                return True
    elif direction == Direction.S:
        for delta in [-1, 1]:
            if grid.coord_blocked(row, col + delta) \
                    and not grid.coord_blocked(row + 1, col + delta):
                return True
    elif direction == Direction.W:
        for delta in [-1, 1]:
            if grid.coord_blocked(row + delta, col) \
                    and not grid.coord_blocked(row + delta, col - 1):
                return True
    elif direction == Direction.E:
        for delta in [-1, 1]:
            if grid.coord_blocked(row + delta, col) \
                    and not grid.coord_blocked(row + delta, col + 1):
                return True
    elif direction == Direction.NW:
        if grid.coord_blocked(row, col + 1) \
                and not grid.coord_blocked(row - 1, col + 1):
            return True
    elif direction == Direction.NE:
        if grid.coord_blocked(row, col - 1) \
                and not grid.coord_blocked(row - 1, col - 1):
            return True
    elif direction == Direction.SW:
        if grid.coord_blocked(row, col + 1) \
                and grid.coord_blocked(row + 1, col + 1):
            return True
    elif direction == Direction.SE:
        if grid.coord_blocked(row, col - 1) \
                and not grid.coord_blocked(row + 1, col - 1):
            return True
    return False


def has_forced_orthogonal_neighbor(grid: Grid, node: Node, direction: Direction) -> bool:
    row, col = grid.node2coord[node.name]
    if direction == Direction.N:
        for delta in [-1, 1]:
            if grid.coord_blocked(row + 1, col + delta) \
                    and not grid.coord_blocked(row, col + delta):
                return True
    elif direction == Direction.S:
        for delta in [-1, 1]:
            if grid.coord_blocked(row - 1, col + delta) \
                    and not grid.coord_blocked(row, col + delta):
                return True
    elif direction == Direction.W:
        for delta in [-1, 1]:
            if grid.coord_blocked(row + delta, col + 1) \
                    and not grid.coord_blocked(row + delta, col):
                return True
    elif direction == Direction.E:
        for delta in [-1, 1]:
            if grid.coord_blocked(row + delta, col - 1) \
                    and not grid.coord_blocked(row + delta, col):
                return True


class JumpPointSearch(BaseFinder):
    def __init__(self, distance="manhattan"):
        super().__init__(PriorityFinderQueue())
        self.diagonal_directions = [Direction.NW, Direction.SW, Direction.SE, Direction.NE]
        self.non_diagonal_directions = [Direction.N, Direction.W, Direction.S, Direction.E]
        self.ns_directions = [Direction.N, Direction.S]
        self.ew_directions = [Direction.E, Direction.W]
        self.distance_method = distance

    def iter_explore(self, graph: Grid, start: str, end: str):
        if not isinstance(graph, Grid):
            raise TypeError(
                "graph must by Grid. Use pathfind.transform.matrix2graph(map, diagonal=True) to convert your map."
                "Or define your map by using pathfind.Grid()")

        self.start = self.init_start = graph.nodes[start]
        self.end = self.init_end = graph.nodes[end]

        self.queue.put(self.start, self.heuristic(self.start))
        visited = set()

        while not self.queue.empty():
            src_node: Node = self.queue.get()

            # expand src node
            visited.add(src_node.name)
            if graph.has_diagonal:
                done = self.explore_with_diagonal(graph, src_node, visited)
            else:
                done = self.explore_orthogonal(graph, src_node, visited)
            if not done:
                yield None
            else:
                return

    def explore_orthogonal(self, graph: Grid, src_node: Node, visited: set) -> bool:
        done = self.expand_ns(graph, src_node, visited)
        if done:
            return True

        done = self.expand_ew(graph, src_node, visited)
        return done

    def expand_ns(self, graph: Grid, src_node: Node, visited: set) -> bool:
        for d in self.ns_directions:
            n = src_node
            while True:
                # scan to north and south
                n = self.scan_orthogonal(graph, n, d, visited)
                if n is self.end:
                    return True
                if n is None:
                    break
                # scan horizontally
                done = self.expand_ew(graph, n, visited)
                if done:
                    return True
        return False

    def expand_ew(self, graph: Grid, src_node: Node, visited: set) -> bool:
        for d in self.ew_directions:
            n = src_node
            while True:
                n = self.scan_orthogonal(graph, n, d, visited)
                if n is self.end:
                    return True
                if n is None:
                    break
        return False

    def scan_orthogonal(self, graph: Grid, node: Node, direction: Direction, visited: set) -> tp.Optional[Node]:
        n_ = graph.get_directed_neighbor(node, direction)
        if n_ is None or n_.name in visited:
            return None
        self.came_from[n_.name] = node
        visited.add(n_.name)
        if has_forced_orthogonal_neighbor(graph, node=n_, direction=direction):
            self.queue.put(n_, self.heuristic(n_))
            return None
        return n_

    def explore_with_diagonal(self, graph: Grid, src_node: Node, visited: set) -> bool:
        done = self.expand_non_diagonal(graph, src_node, visited)
        if done:
            return True

        # expand diagonal
        done = self.expand_diagonal(graph, src_node, visited)
        return done

    def expand_diagonal(self, graph: Grid, src_node: Node, visited: set) -> bool:
        for d in self.diagonal_directions:
            n = src_node
            while True:
                # scan to each direction
                n = self.scan_with_diagonal(graph, n, d, visited)
                if n is self.end:
                    return True
                if n is None:
                    break
                # scan vertically and horizontally
                done = self.expand_non_diagonal(graph, n, visited)
                if done:
                    return True
        return False

    def expand_non_diagonal(self, graph: Grid, src_node: Node, visited: set) -> bool:
        for d in self.non_diagonal_directions:
            n = src_node
            while True:
                n = self.scan_with_diagonal(graph, n, d, visited)
                if n is self.end:
                    return True
                if n is None:
                    break
        return False

    def scan_with_diagonal(self, graph, node: Node, direction, visited) -> tp.Optional[Node]:
        n_ = graph.get_directed_neighbor(node, direction)
        if n_ is None or n_.name in visited:
            return None
        self.came_from[n_.name] = node
        visited.add(n_.name)
        if has_forced_neighbor(graph, node=n_, direction=direction):
            self.queue.put(n_, self.heuristic(n_))
            return None
        return n_

    def check_neighbors(self, current: Node):
        raise NotImplemented

    def heuristic(self, node: Node) -> float:
        return tool.distance(node, self.end, self.distance_method)


class JPS(JumpPointSearch):
    pass
