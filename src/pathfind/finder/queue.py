__all__ = ["PriorityFinderQueue", "LifoFinderQueue", "FifoFinderQueue"]

import heapq
import typing as tp
from abc import ABCMeta, abstractmethod
from collections import deque

from pathfind.graph.graph import Node


class BaseQueue(metaclass=ABCMeta):
    @abstractmethod
    def put(self, item: Node, *args):
        pass

    @abstractmethod
    def get(self) -> tp.Any:
        pass

    @abstractmethod
    def empty(self) -> bool:
        pass

    @abstractmethod
    def clear(self):
        pass


class FifoFinderQueue(BaseQueue):
    def __init__(self):
        self.q = deque()

    def put(self, item: Node, *args):
        self.q.append(item)

    def get(self) -> Node:
        return self.q.popleft()

    def empty(self) -> bool:
        return len(self.q) == 0

    def clear(self):
        self.q.clear()


class LifoFinderQueue(BaseQueue):
    def __init__(self):
        self.q = deque()

    def put(self, item: Node, *args):
        self.q.append(item)

    def get(self) -> Node:
        return self.q.pop()

    def empty(self) -> bool:
        return len(self.q) == 0

    def clear(self):
        self.q.clear()


class PriorityFinderQueue(BaseQueue):
    def __init__(self):
        self.q = []
        heapq.heapify([])
        self.nodes = {}

    def put(self, item: Node, *weight):
        self.nodes[item.name] = item
        weights = []
        for w in weight:
            if isinstance(w, (list, tuple)):
                weights += list(w)
            else:
                weights.append(w)
        heapq.heappush(self.q, (*weights, item.name))

    def get(self) -> Node:
        node_name = heapq.heappop(self.q)[-1]
        return self.nodes[node_name]

    def empty(self) -> bool:
        return len(self.q) == 0

    def clear(self):
        self.q.clear()
        self.nodes.clear()
        heapq.heapify(self.q)
