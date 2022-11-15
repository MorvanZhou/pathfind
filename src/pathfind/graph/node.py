from __future__ import annotations

import math
import typing as tp
from dataclasses import dataclass, field

if tp.TYPE_CHECKING:
    from pathfind.graph.edge import Edge

_GLOBAL_NAME_COUNT = 0


def _get_node_name():
    global _GLOBAL_NAME_COUNT
    name = f"n{_GLOBAL_NAME_COUNT}"
    _GLOBAL_NAME_COUNT += 1
    return name


def _reset_global_name_count():
    global _GLOBAL_NAME_COUNT
    _GLOBAL_NAME_COUNT = 0


@dataclass
class LinkedNode:
    node: Node
    back: bool
    edge: Edge

    @property
    def weight(self):
        if self.back:
            return self.edge.back_weight
        else:
            return self.edge.weight


@dataclass
class Node:
    name: str = field(default_factory=_get_node_name)
    edges: tp.Dict[str, Edge] = field(default_factory=dict)
    _neighbors: tp.Dict[str, LinkedNode] = field(default_factory=dict)
    position: tp.Sequence[float] = field(default_factory=tuple)

    def link(self, edge: Edge):
        self.edges[edge.id] = edge
        if edge.node2 is self:
            if edge.back_weight >= 0:
                ln = LinkedNode(node=edge.node1, back=True, edge=edge)
                self._neighbors[edge.id] = ln
        else:
            if edge.weight >= 0:
                ln = LinkedNode(node=edge.node2, back=False, edge=edge)
                self._neighbors[edge.id] = ln

    def get_neighbor(self, edge: str) -> Node:
        return self.get_neighbor_with_weight(edge).node

    def get_neighbor_with_weight(self, edge: str) -> LinkedNode:
        return self._neighbors[edge]

    @property
    def neighbors(self) -> tp.List[Node]:
        return [ln.node for ln in self._neighbors.values()]

    @property
    def neighbors_with_weight(self):
        return self._neighbors.values()

    def distance_to(self, node: Node) -> float:
        return self.euclidean_distance(node)

    def euclidean_distance(self, node: Node) -> float:
        d = 0
        for i, j in zip(node.position, self.position):
            d += math.pow(i - j, 2)
        return math.sqrt(d)

    def manhattan_distance(self, node: Node) -> float:
        d = 0
        for i, j in zip(node.position, self.position):
            d += abs(i - j)
        return d

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
