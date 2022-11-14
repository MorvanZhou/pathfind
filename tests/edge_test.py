import unittest

import pathfind


class EdgeTest(unittest.TestCase):
    def test_edge(self):
        n1 = pathfind.Node(name="w2")
        n2 = pathfind.Node(name="w1")
        e = pathfind.Edge(node1=n1, node2=n2, weight=0.2)

        self.assertEqual(n1, e.node1)
        self.assertEqual(n2, e.node2)
        self.assertEqual(0.2, e.weight)
        self.assertEqual(0.2, e.weight_back)
        self.assertEqual("w1:w2", e.id)

    def test_define_2_costs(self):
        n1 = pathfind.Node()
        n2 = pathfind.Node()
        e = pathfind.Edge(node1=n1, node2=n2, weight=0.2, weight_back=0.1)

        self.assertEqual(n1, e.node1)
        self.assertEqual(n2, e.node2)
        self.assertEqual(0.2, e.weight)
        self.assertEqual(0.1, e.weight_back)
