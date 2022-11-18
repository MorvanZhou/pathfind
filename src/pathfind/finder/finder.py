from __future__ import annotations

import typing as tp
from abc import ABCMeta, abstractmethod

from pathfind.graph.edge import INFINITY
from pathfind.graph.graph import Graph, Node

if tp.TYPE_CHECKING:
    from pathfind.finder.queue import BaseQueue

NodeName = str
Cost = float
GMap = tp.Dict[NodeName, Cost]
NodeTrace = tp.Dict[NodeName, Node]
GraphPath = tp.List[NodeName]


class BaseFinder(metaclass=ABCMeta):
    def __init__(self, queue: tp.Optional[BaseQueue] = None):
        self.queue = queue
        self._g: GMap = {}  # cost from search start
        self.came_from: NodeTrace = {}  # key: node name, value: parent node
        self.start: tp.Optional[Node] = None
        self.end: tp.Optional[Node] = None
        self.init_start: tp.Optional[Node] = None
        self.init_end: tp.Optional[Node] = None

    def find(self, graph: Graph, start: str, end: str) -> GraphPath:
        explored = self.explore(graph, start, end)
        graph_path = self.traceback(explored)
        return graph_path

    def explore(self, graph: Graph, start: str, end: str) -> NodeTrace:
        # clear when redoing search
        e = self.iter_explore(graph, start, end)
        for _ in e:
            pass
        return self.came_from

    def iter_explore(self, graph: Graph, start: str, end: str) -> tp.Optional[GMap]:
        # clear when redoing search
        self.clear()

        self.start = self.init_start = graph.nodes[start]
        self.end = self.init_end = graph.nodes[end]

        self.queue.put(self.start, 0)
        self.set_g(self.start, 0)
        new_g = {}

        while not self.queue.empty():
            current: Node = self.queue.get()
            if current is self.end:
                break
            self.check_neighbors(current)
            yield {k: self._g[k] for k in self._g.keys() - new_g}
            new_g.update(self._g)

    @abstractmethod
    def check_neighbors(self, current: Node):
        pass

    def set_g(self, node: Node, g: tp.Optional[float] = None):
        if g is None:
            g = -1
        self._g[node.name] = g

    def g(self, node: Node) -> float:
        try:
            return self._g[node.name]
        except KeyError:
            self._g[node.name] = INFINITY
            return self._g[node.name]

    def heuristic(self, node: Node) -> float:
        return 0.

    def h(self, node: Node) -> float:
        return self.heuristic(node)

    def is_visited(self, node: Node) -> bool:
        return node.name in self._g

    def traceback(self, explored: NodeTrace) -> GraphPath:
        trace_start_name = self.init_end.name
        target_name = self.init_start.name
        nodes = [trace_start_name]

        while True:
            parent_node = explored[trace_start_name]
            nodes.insert(0, parent_node.name)
            if parent_node.name == target_name:
                break
            trace_start_name = parent_node.name
        return nodes

    @staticmethod
    def successors(node: Node):
        for edge in node.edges.values():
            successor_with_weight = node.get_successor_with_weight(edge)
            yield successor_with_weight

    @staticmethod
    def predecessors(node: Node):
        for edge in node.edges.values():
            predecessor_with_weight = node.get_predecessor_with_weight(edge)
            yield predecessor_with_weight

    def clear(self):
        if self.queue is not None:
            self.queue.clear()
        self._g.clear()
        self.came_from.clear()
        self.start = None
        self.end = None
        self.init_end = None
        self.init_start = None
