from __future__ import annotations

import typing as tp
from abc import ABCMeta, abstractmethod
from collections import deque

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
        """
        Explore the graph and find a path from start to end point

        Args:
            graph (Graph): graph
            start (str): start node's name
            end (str): end node's name

        Returns:
            GraphPath: a list of node's name (str)
        """
        if start == end:
            return []
        explored = self.explore(graph, start, end)
        if len(explored) == 0 or end not in explored:
            return []
        graph_path = self.traceback(explored)
        return graph_path

    def explore(self, graph: Graph, start: str, end: str) -> NodeTrace:
        """
        Explore the graph from start point, get a traceback dictionary at the end.

        Args:
            graph (Graph): graph
            start (str): start node's name
            end (str): end node's name

        Returns:
            NodeTrace: a dictionary with key of node's name and value of :class:`~Node`, this is used for traceback
        """
        # clear when redoing search
        deque(self.iter_explore(graph, start, end), maxlen=0)

        return self.came_from

    def iter_explore(self, graph: Graph, start: str, end: str, return_cost: bool = False) -> tp.Optional[GMap]:
        """
        Iterate exploring the graph. Return a generator. Please use it in a loop.

        Args:
            graph (Graph): graph
            start (str): start node's name
            end (str): end node's name
            return_cost (bool): whether to return cost

        Returns:
            GMap: a dictionary of node's name and its cost
        """
        # clear when redoing search
        self.clear()

        self.start = self.init_start = graph.nodes[start]
        self.end = self.init_end = graph.nodes[end]

        self.queue.put(self.start, 0)
        self._g[self.start.name] = 0
        new_g = {}

        while not self.queue.empty():
            current: Node = self.queue.get()
            if current is self.end:
                break
            self.check_neighbors(current)
            if return_cost:
                cost = {k: self._g[k] for k in self._g.keys() - new_g}
                new_g.update(self._g)
            else:
                cost = None
            yield cost

    def next(self, graph: Graph, start: str, end: str) -> str:
        """
        Next point to move on. This will compute complete path from start to end, then take the next point from start.

        Args:
            graph (Graph): graph
            start (str): start node's name
            end (str): end node's name

        Returns:
            str: next node's name
        """
        path = self.find(graph=graph, start=start, end=end)
        if len(path) <= 1:
            return start
        return path[1]

    @abstractmethod
    def check_neighbors(self, current: Node):
        pass

    def traceback(self, explored: NodeTrace) -> GraphPath:
        """
        Traceback and get the shortest path from NodeTrace

        Args:
            explored (NodeTrace): a dictionary: key indicates node's name, value represents :class:`~Node`

        Returns:
            GraphPath: a list of node's name (str)
        """
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

    def clear(self):
        if self.queue is not None:
            self.queue.clear()
        self._g.clear()
        self.came_from.clear()
        self.start = None
        self.end = None
        self.init_end = None
        self.init_start = None
