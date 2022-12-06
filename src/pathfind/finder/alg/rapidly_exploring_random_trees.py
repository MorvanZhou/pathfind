import random
import typing as tp

from pathfind.finder import tool
from pathfind.finder.finder import BaseFinder, NodeTrace
from pathfind.finder.queue import FifoFinderQueue
from pathfind.graph import Grid, Node


class RapidlyExploringRandomTrees(BaseFinder):
    def __init__(self, max_expand=5, trace_number=2, distance="manhattan"):
        super().__init__(FifoFinderQueue())
        self.max_expand = max_expand
        self.trace_number = trace_number
        self.distance_method = distance
        self.trace_chain: tp.Dict[str, tp.Tuple[Node, NodeTrace]] = {}

    def check_neighbors(self, current: Node):
        raise NotImplemented

    def iter_explore(self, graph: Grid, start: str, end: str) -> tp.Optional[NodeTrace]:
        if not isinstance(graph, Grid):
            raise TypeError(
                "graph must by Grid. Use pathfind.transform.matrix2graph(map, diagonal=True) to convert your map."
                "Or define your map by using pathfind.Grid()")
        self.start = self.init_start = graph.nodes[start]
        self.end = self.init_end = graph.nodes[end]

        self.queue.put(self.start, self.heuristic(self.start))

        done = False
        while True:
            n = self.queue.get()
            for _ in range(self.trace_number):
                new_n = self.random_next_node(graph, n)
                if new_n is self.end:
                    done = True
                    break
                self.queue.put(new_n, self.heuristic(new_n))
            if done:
                break

        n = self.end

        while True:
            _n, came_from = self.trace_chain[n.name]
            while True:
                close_n = came_from[n.name]
                self.came_from[n.name] = close_n
                yield
                if close_n is _n:
                    break
                n = close_n
            n = _n
            if close_n is self.start:
                return

    def random_next_node(self, graph: Grid, node: Node) -> Node:
        rollout = 5
        while rollout > 0:
            rollout -= 1
            n = node
            trace = {}
            direction = random.randint(0, 3)
            for _ in range(self.max_expand):
                dr, dc = self.move_drdc(direction, graph.has_diagonal)
                current_r, current_c = graph.get_node_coord(n)
                new_r = current_r + dr
                new_c = current_c + dc
                if graph.coord_blocked(new_r, new_c):
                    if len(trace) == 0 or n.name in self.trace_chain:
                        # trace.clear()
                        break
                    self.trace_chain[n.name] = (node, trace)
                    return n
                new_node = graph.get_node_by_coord(new_r, new_c)
                trace[new_node.name] = n
                n = new_node
        return graph.get_node(random.choice(list(self.trace_chain.keys())))

    @staticmethod
    def move_drdc(direction: int, has_diagonal: bool):
        if direction == 0:
            dr = random.randint(0, 1)
            if dr == 0:
                dc = 1
            else:
                dc = 0 if not has_diagonal else random.randint(0, 1)
        elif direction == 1:
            dr = random.randint(0, 1)
            if dr == 0:
                dc = -1
            else:
                dc = 0 if not has_diagonal else random.randint(-1, 0)
        elif direction == 2:
            dr = random.randint(-1, 0)
            if dr == 0:
                dc = -1
            else:
                dc = 0 if not has_diagonal else random.randint(-1, 0)
        else:
            dr = random.randint(-1, 0)
            if dr == 0:
                dc = 1
            else:
                dc = 0 if not has_diagonal else random.randint(0, 1)
        return dr, dc

    def heuristic(self, node: Node) -> float:
        return tool.distance(node, self.end, self.distance_method)


class RRTs(RapidlyExploringRandomTrees):
    pass
