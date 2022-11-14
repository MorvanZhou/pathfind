from __future__ import annotations
import typing as tp
from abc import ABCMeta, abstractmethod

from pathfind.graph.graph import Graph, Node

if tp.TYPE_CHECKING:
    from pathfind.finder.frontier import Frontier


NodeTrace = tp.Dict[str, Node]
GraphPath = tp.List[str]


class BaseFinder(metaclass=ABCMeta):
    def __init__(self, frontier: Frontier):
        self.frontier = frontier
        self._cost_so_far: tp.Dict[str, float] = {}
        self.came_from: NodeTrace = {}      # key: node name, value: parent node
        self.start: tp.Optional[Node] = None
        self.end: tp.Optional[Node] = None

    def find(self, graph: Graph, start: str, end: str) -> GraphPath:
        explored = self.explore(graph, start, end)
        graph_path = self.traceback(start, end, explored)
        return graph_path

    def explore(self, graph: Graph, start: str, end: str) -> NodeTrace:
        self.clear()

        self.frontier.set_nodes(graph_nodes=graph.nodes)
        self.start = graph.nodes[start]
        self.end = graph.nodes[end]

        self.frontier.put(self.start, 0)
        self.reset_cost_to(self.start, 0)

        while not self.frontier.empty():
            current: Node = self.frontier.get()
            if current is self.end:
                break
            self.check_neighbors(current)

        return self.came_from

    @abstractmethod
    def check_neighbors(self, current: Node):
        pass

    def cost_to(self, current: Node) -> float:
        return self._cost_so_far[current.name]

    def reset_cost_to(self, node: Node, cost: float):
        self._cost_so_far[node.name] = cost

    def in_cost_record(self, node: Node) -> bool:
        return node.name in self._cost_so_far

    @staticmethod
    def traceback(start, end, explored: NodeTrace) -> GraphPath:
        nodes = [end]
        while True:
            parent_node = explored[end]
            nodes.insert(0, parent_node.name)
            if parent_node.name == start:
                break
            end = parent_node.name
        return nodes

    @staticmethod
    def neighbors(current: Node):
        for edge in current.edges.values():
            neighbor = current.get_neighbor(edge.id)
            yield neighbor, edge.weight

    def clear(self):
        self.frontier.clear()
        self._cost_so_far.clear()
        self.came_from.clear()
        self.start = None
        self.end = None
