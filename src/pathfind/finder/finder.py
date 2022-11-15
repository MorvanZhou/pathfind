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
        self._cost_dict: tp.Dict[str, float] = {}
        self.came_from: NodeTrace = {}  # key: node name, value: parent node
        self.start: tp.Optional[Node] = None
        self.end: tp.Optional[Node] = None

    def find(self, graph: Graph, start: str, end: str) -> GraphPath:
        explored = self.explore(graph, start, end)
        graph_path = self.traceback(start, end, explored)
        return graph_path

    def explore(self, graph: Graph, start: str, end: str) -> NodeTrace:
        self.clear()

        self.start = graph.nodes[start]
        self.end = graph.nodes[end]

        self.frontier.put(self.start, 0)
        self.discover(self.start, 0)

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
        return self._cost_dict[current.name]

    def discover(self, node: Node, cost: tp.Optional[float] = None):
        if cost is None:
            cost = -1
        self._cost_dict[node.name] = cost

    def is_discovered(self, node: Node) -> bool:
        return node.name in self._cost_dict

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
            neighbor_with_weight = current.get_neighbor_with_weight(edge.id)
            yield neighbor_with_weight.node, neighbor_with_weight.weight

    def clear(self):
        self.frontier.clear()
        self._cost_dict.clear()
        self.came_from.clear()
        self.start = None
        self.end = None
