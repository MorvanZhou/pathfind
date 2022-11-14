import unittest

import pathfind


class TransformTest(unittest.TestCase):
    def test_matrix2graph(self):
        m = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        g = pathfind.transform.matrix2graph(m)
        self.assertEqual(9, len(g.nodes))
        self.assertEqual(12, len(g.edges))
        self.assertEqual(2.5, g.edges["0,0:1,0"].weight)
        self.assertEqual(2.5, g.edges["0,0:1,0"].weight_back)
        self.assertEqual(5.5, g.edges["1,1:1,2"].weight)

    def test_not_connect(self):
        m = [
            [1, -1, 3],
            [4, 5, 6],
            [-1, 8, 9]
        ]
        g = pathfind.transform.matrix2graph(m)
        self.assertEqual(7, len(g.nodes))
        self.assertEqual(7, len(g.edges))
