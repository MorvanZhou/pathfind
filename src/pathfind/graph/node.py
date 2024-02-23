from __future__ import annotations

import typing as tp
from dataclasses import dataclass, field

if tp.TYPE_CHECKING:
    from pathfind.graph.edge import Edge
    from pathfind.graph.portable import Portable

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
    __slots__ = ["node", "edge", "back"]
    node: Node
    edge: Edge
    back: bool

    @property
    def weight(self):
        return self.edge.back_weight if self.back else self.edge.weight


@dataclass
class Node:
    name: str = field(default_factory=_get_node_name)
    edges: tp.Dict[str, Edge] = field(default_factory=dict)
    successors: tp.Dict[str, LinkedNode] = field(default_factory=dict)
    predecessors: tp.Dict[str, LinkedNode] = field(default_factory=dict)
    position: tp.Sequence[float] = field(default_factory=tuple)
    weight: float = field(default=0)
    portables: tp.Dict[str, Portable] = field(default_factory=dict)

    def link(self, edge: Edge):
        if edge.node1 is self:
            if edge.weight >= 0:
                self.successors[edge.id] = LinkedNode(node=edge.node2, edge=edge, back=False)
            if edge.back_weight >= 0:
                self.predecessors[edge.id] = LinkedNode(node=edge.node2, edge=edge, back=True)
        elif edge.node2 is self:
            if edge.weight >= 0:
                self.successors[edge.id] = LinkedNode(node=edge.node1, edge=edge, back=False)
            if edge.back_weight >= 0:
                self.predecessors[edge.id] = LinkedNode(node=edge.node1, edge=edge, back=True)
        else:
            raise ValueError(f"edge does not include this {self.name}")

        self.edges[edge.id] = edge

    def get_all_successors(self) -> tp.List[Node]:
        return [ln.node for ln in self.successors.values()]

    def get_all_successors_with_weight(self) -> tp.List[LinkedNode]:
        return list(self.successors.values())

    def get_predecessor(self, edge: tp.Union[str, Edge]) -> Node:
        return self.get_predecessor_with_weight(edge).node

    def get_predecessor_with_weight(self, edge: tp.Union[str, Edge]) -> LinkedNode:
        if not isinstance(edge, str):
            edge = edge.id
        return self.predecessors[edge]

    def get_all_predecessors(self) -> tp.List[Node]:
        return [ln.node for ln in self.predecessors.values()]

    def get_all_predecessors_with_weight(self) -> tp.List[LinkedNode]:
        return list(self.predecessors.values())

    def add_portable(self, portable: Portable):
        self.portables[portable.name] = portable

    def remove_portable(self, portable: Portable):
        self.portables.pop(portable.name)

    def remove_all_portables(self):
        self.portables.clear()

    @property
    def neighbors(self) -> tp.List[Node]:
        """
        Including both predecessors and successors
        Returns:
            list of Node
        """
        return [ln.node for ln in self.predecessors.values()] + [ln.node for ln in self.successors.values()]

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
