from __future__ import annotations

import typing as tp
from dataclasses import dataclass, field

from pathfind.graph.node import Node

global_nodes = {}
INFINITY = float("inf")


def clear_global_nodes():
    global_nodes.clear()


@dataclass
class Edge:
    node1: tp.Union[Node, str]
    node2: tp.Union[Node, str]
    route_weight: float
    back_route_weight: float = field(default=None)
    id: str = field(default="", init=False)

    def __post_init__(self):
        for attr_name, n in zip(("node1", "node2"), (self.node1, self.node2)):
            if isinstance(n, str):
                try:
                    _n = global_nodes[n]
                except KeyError:
                    _n = Node(name=n)
                    global_nodes[_n.name] = _n
                setattr(self, attr_name, _n)

        self.back_route_weight = self.back_route_weight if self.back_route_weight is not None else self.route_weight
        if self.back_route_weight < 0 and self.route_weight < 0:
            raise ValueError("weight and back_weight cannot be both negative")
        self.id = get_edge_id(self.node1, self.node2)

        self.node1.link(self)
        self.node2.link(self)

    def set_route_weight(self, w: float, back_w: tp.Optional[float] = None):
        if back_w is None:
            back_w = w
        if self.back_route_weight < 0 and self.route_weight < 0:
            raise ValueError("weight and back_weight cannot be both negative")
        self.route_weight = w
        self.back_route_weight = back_w

    @property
    def weight(self):
        return self._add_portable_weight(self.route_weight)

    @property
    def back_weight(self):
        return self._add_portable_weight(self.back_route_weight)

    def _add_portable_weight(self, w: float):
        if len(self.node1.portables) > 0:
            w += sum([p.weight for p in self.node1.portables.values()]) / 2
        if len(self.node2.portables) > 0:
            w += sum([p.weight for p in self.node2.portables.values()]) / 2
        return w

    @property
    def nodes(self) -> tp.List[Node]:
        return [self.node1, self.node2]

    def __repr__(self):
        return self.id

    def __str__(self):
        return self.id


def get_edge_id(node1: tp.Union[str, Node], node2: tp.Union[str, Node]) -> str:
    if isinstance(node1, Node):
        node1 = node1.name
    if isinstance(node2, Node):
        node2 = node2.name
    nodes = sorted({node1, node2})
    return f"{nodes[0]}:{nodes[1]}"
