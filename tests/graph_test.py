import unittest

import pathfind


class GraphTest(unittest.TestCase):
    def test_add_edge(self):
        n1 = pathfind.Node()
        n2 = pathfind.Node()
        n3 = pathfind.Node()
        e1 = pathfind.Edge(node1=n1, node2=n2, weight=0.2)
        e2 = pathfind.Edge(node1=n1, node2=n3, weight=0.1)
        e3 = pathfind.Edge(n2, n3, weight=0)

        g = pathfind.Graph()
        g.add_edges([e1, e2, e3])
        self.assertEqual(3, len(g.edges))
        self.assertEqual(3, len(g.nodes))
        # g.show()

    def test_create_conf(self):
        conf = [
            ["n1", "n2", 0.1],
            ["n1", "n3", 0.2],
            ["n2", "n3", 0.3, 0.4]
        ]
        g = pathfind.Graph(conf)
        self.assertEqual(3, len(g.edges))
        self.assertEqual(3, len(g.nodes))
        self.assertIn("n1:n2", g.edges)
        self.assertEqual(0.1, g.edges["n1:n2"].back_weight)
        self.assertEqual(0.3, g.edges["n2:n3"].weight)
        self.assertEqual(0.4, g.edges["n2:n3"].back_weight)

        # g.show()
