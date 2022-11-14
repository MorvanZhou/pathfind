from __future__ import annotations
import typing as tp
from dataclasses import dataclass, field

if tp.TYPE_CHECKING:
    from pathfind.graph.node import Node


@dataclass
class Edge:
    node1: Node
    node2: Node
    weight: float
    weight_back: float = field(default=None)
    id: str = field(default="")

    def __post_init__(self):
        self.weight_back = self.weight_back if self.weight_back is not None else self.weight
        nodes = sorted({self.node1.name, self.node2.name})
        self.id = f"{nodes[0]}:{nodes[1]}"

        self.node1.link(self)
        self.node2.link(self)

    def __repr__(self):
        return self.id

    def __str__(self):
        return self.id
