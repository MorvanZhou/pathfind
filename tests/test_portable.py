import unittest

import pathfind


class PortableTest(unittest.TestCase):
    def test_add_move(self):
        conf = [
            ["n1", "n2", 0.1],
            ["n1", "n3", 0.2],
            ["n2", "n3", 0.3, 0.4]
        ]
        g = pathfind.Graph(conf)

        p1 = pathfind.Portable(weight=1, name="p1")
        p2 = pathfind.Portable(weight=2, name="p2")

        g.add_portable(node_name="n1", portable=p1)
        g.add_portable(node_name="n2", portable=p2)

        self.assertIn("n1:n2", g.edges)
        self.assertEqual(0.1, g.edges["n1:n2"].back_route_weight)
        self.assertEqual(0.3, g.edges["n2:n3"].route_weight)
        self.assertEqual(0.4, g.edges["n2:n3"].back_route_weight)
        self.assertEqual(1, sum([p.weight for p in g.nodes["n1"].portables.values()]))
        self.assertEqual(2, sum([p.weight for p in g.nodes["n2"].portables.values()]))

        w = 0.1 + 1 / 2 + 2 / 2
        self.assertEqual(w, g.nodes["n1"].successors["n1:n2"].weight)
        self.assertEqual(w, g.nodes["n2"].predecessors["n1:n2"].weight)
        self.assertEqual(
            g.edges["n2:n3"].back_route_weight + p2.weight / 2,
            g.nodes["n3"].predecessors["n2:n3"].weight)

        # move portable
        g.move_portable(portable=p1, new_node_name="n2")
        self.assertEqual(p1.weight + p2.weight, sum([p.weight for p in g.nodes["n2"].portables.values()]))
        self.assertEqual(0, len(g.nodes["n1"].portables))
        self.assertEqual(2, len(g.nodes["n2"].portables))
        self.assertEqual(
            g.edges["n2:n3"].back_route_weight + p2.weight / 2 + p1.weight / 2,
            g.nodes["n3"].predecessors["n2:n3"].weight)

        # remove portable
        g.remove_portable(portable=p2)
        self.assertEqual(p1.weight, sum([p.weight for p in g.nodes["n2"].portables.values()]))
        self.assertEqual(1, len(g.nodes["n2"].portables))
        self.assertEqual(
            g.edges["n2:n3"].back_route_weight + p1.weight / 2,
            g.nodes["n3"].predecessors["n2:n3"].weight)
