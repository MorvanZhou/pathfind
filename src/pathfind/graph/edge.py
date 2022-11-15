from __future__ import annotations

import typing as tp
from dataclasses import dataclass, field

from pathfind.graph.node import Node

global_nodes = {}


def clear_global_nodes():
    global_nodes.clear()


@dataclass
class Edge:
    node1: tp.Union[Node, str]
    node2: tp.Union[Node, str]
    weight: float
    weight_back: float = field(default=None)
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

        self.weight_back = self.weight_back if self.weight_back is not None else self.weight
        if self.weight_back < 0 and self.weight < 0:
            raise ValueError("weight and weight_back cannot be both negative")
        nodes = sorted({self.node1.name, self.node2.name})
        self.id = f"{nodes[0]}:{nodes[1]}"

        self.node1.link(self)
        self.node2.link(self)

    def set_weight(self, weight: float, weight_back: tp.Optional[float] = None):
        if weight_back is None:
            weight_back = weight
        if self.weight_back < 0 and self.weight < 0:
            raise ValueError("weight and weight_back cannot be both negative")
        self.weight = weight
        self.weight_back = weight_back

    @property
    def nodes(self) -> tp.List[Node]:
        return [self.node1, self.node2]

    def __repr__(self):
        return self.id

    def __str__(self):
        return self.id
