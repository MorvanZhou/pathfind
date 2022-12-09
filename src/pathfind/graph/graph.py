from __future__ import annotations

import enum
import math
import typing as tp

import igraph as ig
import matplotlib.pyplot as plt

from pathfind.graph.edge import Edge, get_edge_id, INFINITY
from pathfind.graph.node import Node


class Graph:
    def __init__(self, conf: tp.Optional[tp.Sequence[tp.Sequence]] = None):
        self.nodes: tp.Dict[str, Node] = {}
        self.edges: tp.Dict[str, Edge] = {}
        if conf is not None:
            self.load(conf)

    def clear(self):
        self.nodes.clear()
        self.edges.clear()

    def load(self, conf: tp.Sequence[tp.Sequence]):
        for edge_data in conf:
            n_edge_data = len(edge_data)
            if n_edge_data < 3 or n_edge_data > 6:
                raise ValueError(f"config data shape error, edge config length={n_edge_data}, it should in [3, 6]")
            n_name1, n_name2 = edge_data[:2]
            try:
                position1 = edge_data[4]
            except IndexError:
                position1 = ()
            try:
                position2 = edge_data[5]
            except IndexError:
                position2 = ()
            n1 = Node(name=n_name1, position=position1) if n_name1 not in self.nodes else self.nodes[n_name1]
            n2 = Node(name=n_name2, position=position2) if n_name2 not in self.nodes else self.nodes[n_name2]
            w = edge_data[2]
            try:
                w_back = edge_data[3]
            except IndexError:
                w_back = w
            self.add_edge(Edge(node1=n1, node2=n2, weight=w, back_weight=w_back))

    def add(self, edge: Edge):
        self.add_edge(edge)

    def add_node(self, node: Node):
        if node.name not in self.nodes:
            self.nodes[node.name] = node
        else:
            raise ValueError(f"node of name '{node.name}' have already been added")

    def add_edge(self, edge: Edge):
        if edge.id in self.edges:
            raise ValueError(f"edge.id={edge.id} has been added")

        for n in edge.nodes:
            if n.name in self.nodes:
                if self.nodes[n.name] is not n:
                    raise ValueError(f"two different nodes have the same name '{n.name}'")
            else:
                self.add_node(n)
        self.edges[edge.id] = edge

    def add_edges(self, edges: tp.Sequence[Edge]):
        for edge in edges:
            self.add_edge(edge)

    def get_node(self, name: str) -> Node:
        return self.nodes[name]

    def get_edge(self, eid: str) -> Edge:
        return self.edges[eid]

    def remove_node_by_name(self, name: str):
        if name not in self.nodes:
            return
        node = self.nodes[name]
        for edge_id in node.edges.keys():
            self.remove_edge_by_name(edge_id)
        try:
            del self.nodes[node.name]
        except KeyError:
            pass

    def remove_node(self, node: Node):
        self.remove_node_by_name(node.name)

    def remove_edge_by_name(self, name: str):
        try:
            del self.edges[name]
        except KeyError:
            pass

    def remove_edge(self, edge: Edge):
        self.remove_edge_by_name(edge.id)

    def plot(self, trace: tp.Optional[tp.Sequence[str]] = None):
        g = ig.Graph(directed=False)
        nodes_color = []
        for node in self.nodes.values():
            if trace is None:
                nodes_color.append("#a5d3f5")
            else:
                if node.name in trace:
                    nodes_color.append("#f5b0a4")
                else:
                    nodes_color.append("#a5d3f5")
            g.add_vertex(node.name)
        max_width = 0
        edge_id_set = set()
        if trace is not None:
            for i in range(len(trace) - 1):
                edge_id_set.add(get_edge_id(self.nodes[trace[i]], self.nodes[trace[i + 1]]))
        edges_color = []
        for edge in self.edges.values():
            if edge.weight > max_width:
                max_width = edge.weight
            g.add_edge(edge.node1.name, edge.node2.name, width=edge.weight)
            if edge.id in edge_id_set:
                edges_color.append("#fc5f47")
            else:
                edges_color.append("#cccccc")

        fig, ax = plt.subplots(figsize=(10, 10))

        ig.plot(
            g,
            target=ax,
            layout=g.layout("auto"),
            vertex_size=.3,
            vertex_color=nodes_color,
            vertex_frame_width=3,
            vertex_frame_color="white",
            vertex_label=g.vs["name"],
            vertex_label_size=15,
            edge_color=edges_color,
            edge_width=[2.5 * (w + 7) / (7 + max_width) for w in g.es["width"]],
            # edge_arrow_size=0.02,
            # edge_arrow_width=1,
        )
        return fig

    def show(self, trace=None):
        self.plot(trace)
        plt.show()

    def save_graph(self, path, trace=None):
        fig = self.plot(trace)
        fig.savefig(path)


class Direction(enum.Enum):
    N = 0
    W = enum.auto()
    S = enum.auto()
    E = enum.auto()
    NW = enum.auto()
    SW = enum.auto()
    SE = enum.auto()
    NE = enum.auto()

    @staticmethod
    def opposite(d: Direction) -> Direction:
        return _OPPOSITE[d]


_OPPOSITE = {
    Direction.N: Direction.S,
    Direction.S: Direction.N,
    Direction.W: Direction.E,
    Direction.E: Direction.W,
    Direction.NW: Direction.SE,
    Direction.SW: Direction.NE,
    Direction.SE: Direction.NW,
    Direction.NE: Direction.SW,
}


class Grid(Graph):
    dire2delta = {
        Direction.N: (-1, 0),
        Direction.W: (0, -1),
        Direction.S: (1, 0),
        Direction.E: (0, 1),
        Direction.NW: (-1, -1),
        Direction.SW: (1, -1),
        Direction.SE: (1, 1),
        Direction.NE: (-1, 1),
    }

    def __init__(self, conf: tp.Optional[tp.Sequence[tp.Sequence]] = None, has_diagonal: bool = False):
        super().__init__(conf=conf)
        self.grid: tp.List[tp.List[Node]] = []
        self.node2coord: tp.Dict[str, tp.Tuple[int, int]] = {}
        self.has_diagonal = has_diagonal

    def load(self, conf: tp.Sequence[tp.Sequence]):
        pass

    @property
    def height(self) -> int:
        return len(self.grid)

    @property
    def width(self) -> int:
        return len(self.grid[0])

    def add_node_by_coord(self, row: int, col: int, weight: float):
        try:
            self.grid[row]
        except IndexError:
            self.grid += [[] * (row + 1 - self.height)]

        try:
            self.grid[row][col]
        except IndexError:
            self.grid[row] += [None for _ in range(col + 1 - len(self.grid[row]))]

        if self.grid[row][col] is None:
            n = Node(f"{row},{col}", position=(row, col), weight=weight)
            self.grid[row][col] = n
            self.node2coord[n.name] = (row, col)
            self._try_add_top_left_edge(node=n)

    def _try_add_top_left_edge(self, node: Node):
        self.add_node(node)
        node_row = int(node.position[0])
        node_col = int(node.position[1])
        to_be_added = []
        if node_row >= 1:
            n2 = self.get_node_by_coord(node_row - 1, node_col)
            w = (node.weight + n2.weight) / 2
            to_be_added.append([n2, w])
        if node_col >= 1:
            n2 = self.get_node_by_coord(node_row, node_col - 1)
            w = (node.weight + n2.weight) / 2
            to_be_added.append([n2, w])
        if self.has_diagonal:
            if node_row >= 1 and node_col + 1 < len(self.grid[node_row - 1]):
                n2 = self.get_node_by_coord(node_row - 1, node_col + 1)
                w = math.sqrt(node.weight ** 2 + n2.weight ** 2)
                to_be_added.append([n2, w])
            if node_row >= 1 and node_col >= 1:
                n2 = self.get_node_by_coord(node_row - 1, node_col - 1)
                w = math.sqrt(node.weight ** 2 + n2.weight ** 2)
                to_be_added.append([n2, w])
        for n2 in to_be_added:
            e = Edge(node1=node, node2=n2[0], weight=n2[1], back_weight=n2[1])
            self.edges[e.id] = e

    def get_node_by_coord(self, row: int, col: int):
        return self.grid[row][col]

    def get_edge_by_coord(self, r1: int, c1: int, r2: int, c2: int):
        return self.edges[f"{r1},{c1}:{r2},{c2}"]

    def get_directed_neighbor(self, node: Node, direction: Direction) -> tp.Optional[Node]:
        row, col = self.node2coord[node.name]
        dr, dc = self.dire2delta[direction]
        new_row, new_col = row + dr, col + dc
        if new_row < 0 or new_col < 0:
            return None
        try:
            n = self.grid[new_row][new_col]
            if n.weight == INFINITY:
                return None
            return n
        except IndexError:
            return None

    def get_node_coord(self, node: Node) -> tp.Tuple[int, int]:
        return self.node2coord[node.name]

    def coord_blocked(self, row: int, col: int) -> bool:
        if row < 0 or col < 0 or row >= self.height or col >= self.width:
            return True
        return self.grid[row][col].weight == INFINITY
