from __future__ import annotations

import math
import typing as tp

if tp.TYPE_CHECKING:
    from pathfind.graph.graph import Node


def euclidean_distance(node1: Node, node2: Node) -> float:
    d = 0
    for i, j in zip(node1.position, node2.position):
        d += math.pow(i - j, 2)
    return math.sqrt(d)


def manhattan_distance(node1: Node, node2: Node) -> float:
    d = 0
    for i, j in zip(node1.position, node2.position):
        d += abs(i - j)
    return d


def chebyshev_distance(node1: Node, node2: Node) -> float:
    ds = []
    for i, j in zip(node1.position, node2.position):
        ds.append(abs(i - j))
    return sum(ds) - min(ds)


def octile_distance(node1: Node, node2: Node) -> float:
    ds = []
    for i, j in zip(node1.position, node2.position):
        ds.append(abs(i - j))
    return sum(ds) + (math.sqrt(2) - 2) * min(ds)


DISTANCE_MAP: tp.Dict[str, tp.Callable[[Node, Node], float]] = {
    "euclidean": euclidean_distance,
    "manhattan": manhattan_distance,
    "chebyshev": chebyshev_distance,
    "octile": octile_distance,
}


def distance(node1: Node, node2: Node, method: str) -> float:
    return DISTANCE_MAP[method](node1, node2)
