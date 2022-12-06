import math
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
        self.assertEqual(2.5, g.edges["0,0:1,0"].back_weight)
        self.assertEqual(5.5, g.edges["1,1:1,2"].weight)

    def test_not_connect(self):
        m = [
            [1, -1, 3],
            [4, 5, 6],
            [-1, 8, 9]
        ]
        g = pathfind.transform.matrix2graph(m)
        self.assertEqual(9, len(g.nodes))
        self.assertEqual(12, len(g.edges))

    def test_infinity(self):
        m = [
            [1, pathfind.INFINITY, 3],
            [4, 5, 6],
            [pathfind.INFINITY, 8, 9]
        ]
        g = pathfind.transform.matrix2graph(m)
        # g.show()
        self.assertEqual(9, len(g.nodes))
        self.assertEqual(12, len(g.edges))
        self.assertEqual(pathfind.INFINITY, g.edges["2,0:2,1"].weight)

    def test_diagonally(self):
        m = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ]
        g = pathfind.transform.matrix2graph(m, diagonal=True)
        # g.show()
        self.assertEqual(9, len(g.nodes))
        self.assertEqual(12 + 2 * 4, len(g.edges))
        self.assertAlmostEqual(math.sqrt(2), g.edges["0,2:1,1"].weight)
