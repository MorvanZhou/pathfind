__all__ = ["PriorityFinderQueue", "LifoFinderQueue", "FifoFinderQueue"]

import typing as tp
from abc import ABCMeta, abstractmethod
from queue import PriorityQueue, Empty, LifoQueue, Queue

from pathfind.graph.graph import Node


class BaseQueue(metaclass=ABCMeta):
    def __init__(self, q: Queue):
        self.q: Queue = q

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

    def _clear(self):
        while not self.q.empty():
            try:
                self.q.get(False)
            except Empty:
                continue
            self.q.task_done()


class FifoFinderQueue(BaseQueue):
    def __init__(self):
        super().__init__(Queue())

    def put(self, item: Node, *args):
        self.q.put(item)

    def get(self) -> Node:
        return self.q.get()

    def empty(self) -> bool:
        return self.q.empty()

    def clear(self):
        self._clear()


class LifoFinderQueue(BaseQueue):
    def __init__(self):
        super().__init__(LifoQueue())

    def put(self, item: Node, *args):
        self.q.put(item)

    def get(self) -> Node:
        return self.q.get()

    def empty(self) -> bool:
        return self.q.empty()

    def clear(self):
        self._clear()


class PriorityFinderQueue(BaseQueue):
    def __init__(self):
        super().__init__(PriorityQueue())
        self.nodes = {}

    def put(self, item: Node, *weight):
        self.nodes[item.name] = item
        weights = []
        for w in weight:
            if isinstance(w, (list, tuple)):
                weights += list(w)
            else:
                weights.append(w)
        self.q.put((*weights, item.name))

    def get(self) -> Node:
        node_name = self.q.get()[-1]
        return self.nodes[node_name]

    def empty(self) -> bool:
        return self.q.empty()

    def clear(self):
        self.nodes.clear()
