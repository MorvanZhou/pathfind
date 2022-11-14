from __future__ import annotations

import typing as tp

import igraph as ig
import matplotlib.pyplot as plt

from pathfind.graph.edge import Edge
from pathfind.graph.node import Node


class Graph:
    def __init__(self, conf: tp.Optional[tp.Sequence[tp.Sequence]] = None):
        self.nodes: tp.Dict[str, Node] = {}
        self.edges: tp.Dict[str, Edge] = {}
        if conf is not None:
            self.load(conf)

    def load(self, conf: tp.Sequence[tp.Sequence]):
        for edge_data in conf:
            n_edge_data = len(edge_data)
            if n_edge_data < 3 or n_edge_data > 4:
                raise ValueError(f"config data shape error, edge config length={n_edge_data}, it should in [3, 4]")
            n_name1, n_name2 = edge_data[:2]
            n1 = Node(name=n_name1) if n_name1 not in self.nodes else self.nodes[n_name1]
            n2 = Node(name=n_name2) if n_name2 not in self.nodes else self.nodes[n_name2]
            w = edge_data[2]
            try:
                w_back = edge_data[3]
            except IndexError:
                w_back = w
            self.add_edge(Edge(node1=n1, node2=n2, weight=w, weight_back=w_back))

    def add(self, edge: Edge):
        self.add_edge(edge)

    def add_node(self, node: Node):
        if node.name not in self.nodes:
            self.nodes[node.name] = node
        else:
            if self.nodes[node.name] is not node:
                raise ValueError(f"two different nodes have the same {node.name=}")

    def add_edge(self, edge: Edge):
        if edge.id in self.edges:
            raise ValueError(f"{edge.id=} has been added")
        self.edges[edge.id] = edge
        self.add_node(edge.node1)
        self.add_node(edge.node2)

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

    def __plot(self, trace=None):
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
        for edge in self.edges.values():
            if edge.weight > max_width:
                max_width = edge.weight
            g.add_edge(edge.node1.name, edge.node2.name, width=edge.weight)

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
            edge_color="#cccccc",
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
