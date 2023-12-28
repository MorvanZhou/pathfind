from __future__ import annotations

import typing as tp
from math import pow, sqrt

if tp.TYPE_CHECKING:
    from pathfind.graph.graph import Node

def euclidean_distance(node1: Node, node2: Node) -> float:
    return sqrt(sum(map(lambda x, y: pow(x - y, 2), node1.position, node2.position)))


def manhattan_distance(node1: Node, node2: Node) -> float:
    return sum(map(lambda x, y: abs(x - y), node1.position, node2.position))


def chebyshev_distance(node1: Node, node2: Node) -> float:
    ds = map(lambda x, y: abs(x - y), node1.position, node2.position)
    return sum(ds) - min(ds)


def octile_distance(node1: Node, node2: Node) -> float:
    ds = map(lambda x, y: abs(x - y), node1.position, node2.position)
    return sum(ds) + (sqrt(2) - 2) * min(ds)


DISTANCE_MAP: tp.Dict[str, tp.Callable[[Node, Node], float]] = {
    "euclidean": euclidean_distance,
    "manhattan": manhattan_distance,
    "chebyshev": chebyshev_distance,
    "octile": octile_distance,
}
