from __future__ import annotations

import heapq
import typing as tp

from pathfind.finder import tool
from pathfind.finder.finder import BaseFinder, NodeTrace
from pathfind.graph import Node, Graph, INFINITY

Key = tp.Tuple[float, float]


class DStarQueue:
    REMOVED = '<removed-item>'

    def __init__(self):
        self.pq = []
        self.nodes: tp.Dict[str, Node] = {}
        self.entry_finder: tp.Dict[str, tp.Any] = {}

    def insert(self, u: Node, key: Key):
        if u.name in self.entry_finder:
            self.remove(u)
        entry = [key[0], key[1], u.name]
        self.entry_finder[u.name] = entry
        heapq.heappush(self.pq, entry)
        self.nodes[u.name] = u

    def top(self) -> tp.Tuple[tp.Tuple[float, float], tp.Optional[Node]]:
        while self.pq:
            k0, k1, name = heapq.heappop(self.pq)
            if name is not self.REMOVED:
                del self.entry_finder[name]
                return (k0, k1), self.nodes.pop(name)
        return (INFINITY, INFINITY), None
        # self.pq.sort()
        # if len(self.pq) > 0:
        #     t = self.pq[0]
        #     return (k0, k1), self.nodes[name]
        # else:
        #     return (INFINITY, INFINITY), None

    def update(self, u: Node, key: Key):
        self.insert(u, key)

    def remove(self, item: Node):
        entry = self.entry_finder.pop(item.name)
        entry[-1] = self.REMOVED
        self.nodes.pop(item.name)

    def has(self, item: Node):
        return item.name in self.entry_finder

    def clear(self):
        self.nodes.clear()
        self.entry_finder.clear()
        self.pq.clear()
        heapq.heapify(self.pq)


class DStarLite(BaseFinder):
    def __init__(self, distance="manhattan"):
        super().__init__()
        self.queue = DStarQueue()
        self.km = 0
        self.distance_method = distance
        self._rhs: tp.Dict[str, float] = {}
        self._g: tp.Dict[str, float] = {}
        self._edge_cost: tp.Dict[(str, str), float] = {}

    def initialize(self, graph: Graph, start: str, end: str):
        self.clear()
        self._rhs.clear()
        self.km = 0

        self.start = self.init_start = graph.nodes[start]
        self.end = self.init_end = graph.nodes[end]

        for edge in graph.edges.values():
            self.save_edge_cost(edge.node1, edge.node2, edge.weight)
            self.save_edge_cost(edge.node2, edge.node1, edge.back_weight)

        self.set_rhs(self.end, 0.)
        key = self.h(self.end), 0
        self.queue.insert(self.end, key)

    def key(self, node: Node) -> tp.Tuple[float, float]:
        min_g_rhs = min(self.g(node), self.rhs(node))
        return min_g_rhs + self.h(node) + self.km, min_g_rhs

    def iter_explore(self, graph: Graph, start: str, end: str) -> NodeTrace:
        self.initialize(graph, start, end)
        self.compute_shortest_path()
        last = self.start

        new_g = {}
        while self.start is not self.end:
            if self.rhs(self.start) == INFINITY:
                return {}
            min_cost = INFINITY
            next_node = None
            for s in self.successors(self.start):
                cost = s.weight + self.g(s.node)
                if cost < min_cost:
                    next_node = s.node
                    min_cost = cost

            self.came_from[next_node.name] = self.start
            self.start = next_node
            yield {k: self._g[k] for k, v in self._g.items() if new_g.get(k, None) != v}
            new_g.update(self._g)

            changed = False
            for s in self.successors(self.start):
                # check weight change
                c_old = self.get_edge_cost(self.start, s.node)
                if s.weight != c_old:
                    changed = True
                    self.km += self._heuristic(last, self.start)
                    last = self.start
                    self.save_edge_cost(self.start, s.node, s.weight)
                    if c_old > s.weight:
                        if self.start is not self.end:
                            self.set_rhs(self.start, min(self.rhs(self.start), s.weight + self.g(s.node)))
                    elif self.rhs(self.start) == c_old + self.g(s.node):
                        if self.start is not self.end:
                            self.renew_rhs(self.start)
                    self.update_node(self.start)
            if changed:
                self.compute_shortest_path()

    def update_node(self, u: Node):
        g_equal_rhs = self.g(u) == self.rhs(u)
        has_node = self.queue.has(u)
        if not g_equal_rhs and has_node:
            self.queue.update(u, self.key(u))
        elif not g_equal_rhs and not has_node:
            self.queue.insert(u, self.key(u))
        elif g_equal_rhs and has_node:
            self.queue.remove(u)

    def compute_shortest_path(self):
        while True:
            k_old, u = self.queue.top()
            k_new = self.key(u)
            g = self.g(u)
            rhs = self.rhs(u)
            if k_old < k_new:
                self.queue.update(u, k_new)
            elif g > rhs:
                self.set_g(u, rhs)
                # self.queue.remove(u)  # removed when doing self.queue.top()
                for s in self.predecessors(u):
                    if s.node is not self.end:
                        self.set_rhs(s.node, min(self.rhs(s.node), s.weight + self.g(u)))
                    self.update_node(s.node)
            else:
                g_old = g
                self.set_g(u, INFINITY)
                self.queue.insert(u, k_old)  # add back after self.queue.top()
                for s in self.predecessors(u):
                    if self.rhs(s.node) == s.weight + g_old:
                        if s.node is not self.end:
                            self.renew_rhs(s.node)
                    self.update_node(s.node)
            if not (k_old < self.key(self.start) or self.rhs(self.start) > self.g(self.start)):
                break

    def save_edge_cost(self, n1: Node, n2: Node, c: float):
        self._edge_cost[(n1.name, n2.name)] = c

    def get_edge_cost(self, n1: Node, n2: Node) -> float:
        return self._edge_cost[(n1.name, n2.name)]

    def check_neighbors(self, current: Node):
        raise NotImplemented

    def heuristic(self, node: Node) -> float:
        return self._heuristic(self.start, node)

    def _heuristic(self, n1: Node, n2: Node) -> float:
        return tool.distance(n1, n2, self.distance_method)

    def set_rhs(self, node: Node, rhs: float):
        self._rhs[node.name] = rhs

    def renew_rhs(self, node: Node):
        rhs = INFINITY
        for neighbor in self.successors(node):
            n_rhs = neighbor.weight + self.g(neighbor.node)
            if n_rhs < rhs:
                rhs = n_rhs
        self.set_rhs(node, rhs)

    def rhs(self, node: Node) -> float:
        try:
            return self._rhs[node.name]
        except KeyError:
            self._rhs[node.name] = INFINITY
            return self._rhs[node.name]

    def clear(self):
        self._rhs.clear()
        if self.queue is not None:
            self.queue.clear()
        self._g.clear()
        self.came_from.clear()
        self.start = None
        self.end = None
        self.init_end = None
        self.init_start = None
