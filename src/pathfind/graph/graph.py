from __future__ import annotations

import typing as tp

import igraph as ig
import matplotlib.pyplot as plt

from pathfind.graph.edge import Edge, get_edge_id
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
            raise ValueError(f"{edge.id=} has been added")

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

    def __plot(self, trace: tp.Optional[tp.Sequence[str]] = None):
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

    def plot(self, trace=None):
        self.__plot(trace)
        plt.show()

    def save_graph(self, path, trace=None):
        fig = self.__plot(trace)
        fig.savefig(path)
