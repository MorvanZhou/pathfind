import typing as tp
from abc import ABCMeta, abstractmethod
from collections import deque
from queue import PriorityQueue, Empty

from pathfind.graph.graph import Node


class Frontier(metaclass=ABCMeta):
    def __init__(self):
        self.nodes = {}

    def set_nodes(self, graph_nodes: tp.Dict[str, Node]):
        self.nodes = graph_nodes

    @abstractmethod
    def put(self, item: Node, weight=0):
        pass

    @abstractmethod
    def get(self) -> Node:
        pass

    @abstractmethod
    def empty(self) -> bool:
        pass

    @abstractmethod
    def clear(self):
        pass


class FIFOFrontier(Frontier):
    def __init__(self):
        super().__init__()
        self.q = deque()

    def put(self, item: Node, weight=0):
        self.q.append(item)

    def get(self) -> Node:
        return self.q.popleft()

    def empty(self) -> bool:
        return len(self.q) == 0

    def clear(self):
        self.nodes.clear()
        self.q.clear()


class FILOFrontier(FIFOFrontier):
    def __init__(self):
        super().__init__()
        self.q = deque()

    def get(self) -> Node:
        return self.q.pop()


class PriorityFrontier(Frontier):
    def __init__(self):
        super().__init__()
        self.q = PriorityQueue()

    def put(self, item: Node, weight=0):
        self.q.put((weight, item.name))

    def get(self) -> Node:
        node_name = self.q.get()[1]
        return self.nodes[node_name]

    def empty(self) -> bool:
        return self.q.empty()

    def clear(self):
        self.nodes.clear()
        while not self.q.empty():
            try:
                self.q.get(False)
            except Empty:
                continue
            self.q.task_done()
