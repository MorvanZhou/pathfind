import unittest

import pathfind


class EdgeTest(unittest.TestCase):
    def setUp(self) -> None:
        pathfind.graph.node._reset_global_name_count()
        pathfind.graph.edge.clear_global_nodes()

    def test_edge(self):
        n1 = pathfind.Node(name="w2")
        n2 = pathfind.Node(name="w1")
        e = pathfind.Edge(node1=n1, node2=n2, weight=0.2)

        self.assertEqual(n1, e.node1)
        self.assertEqual(n2, e.node2)
        self.assertEqual(0.2, e.weight)
        self.assertEqual(0.2, e.weight_back)
        self.assertEqual("w1:w2", e.id)

    def test_negative_weight(self):
        n1 = pathfind.Node()
        n2 = pathfind.Node()
        e1 = pathfind.Edge(node1=n1, node2="customer_name", weight=0.1)
        e2 = pathfind.Edge(n2, "customer_name", weight=0)

        g = pathfind.Graph()
        g.add_edges([e1, e2])
        self.assertEqual(2, len(g.edges))

    def test_define_2_costs(self):
        n1 = pathfind.Node()
        n2 = pathfind.Node()
        e = pathfind.Edge(node1=n1, node2=n2, weight=0.2, weight_back=0.1)

        self.assertEqual(n1, e.node1)
        self.assertEqual(n2, e.node2)
        self.assertEqual(0.2, e.weight)
        self.assertEqual(0.1, e.weight_back)

    def test_name(self):
        my_n0 = pathfind.Node(name="my_n0")  # node name set to "my_n0"
        auto_name = pathfind.Node()  # node name automatically set to "n0"
        n2 = "n2"  # pass a string to represent node name
        e0 = pathfind.Edge(node1=my_n0, node2=auto_name, weight=0.2)
        e1 = pathfind.Edge(node1=my_n0, node2=n2, weight=0.1)
        e2 = pathfind.Edge(auto_name, n2, weight=0)

        g = pathfind.Graph()
        g.add_edges([e0, e1, e2])
        self.assertEqual(3, len(g.edges))
