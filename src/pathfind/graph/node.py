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
class Node:
    name: str = field(default_factory=_get_node_name)
    edges: tp.Dict[str, Edge] = field(default_factory=dict)
    linked_node: tp.Dict[str, Node] = field(default_factory=dict)
    position: tp.Sequence[float] = field(default_factory=tuple)

    def link(self, edge: Edge):
        self.edges[edge.id] = edge
        self.linked_node[edge.id] = edge.node1 if edge.node2 is self else edge.node2

    def get_neighbor(self, edge: str):
        return self.linked_node[edge]

    @property
    def neighbors(self):
        return list(self.linked_node.values())

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
