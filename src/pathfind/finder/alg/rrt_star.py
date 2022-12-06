import typing as tp

from pathfind.finder.finder import BaseFinder, GMap
from pathfind.finder.queue import FifoFinderQueue
from pathfind.graph import Graph, Node


class RapidlyExploringRandomTreesStar(BaseFinder):
    def __init__(self):
        super().__init__(FifoFinderQueue())
        self.max_distance = 10

    def iter_explore(self, graph: Graph, start: str, end: str) -> tp.Optional[GMap]:
        pass

    def check_neighbors(self, current: Node):
        raise NotImplemented


class RRTStar(RapidlyExploringRandomTreesStar):
    pass
