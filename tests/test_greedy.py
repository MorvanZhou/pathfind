import unittest

import pathfind


class GreedyTest(unittest.TestCase):
    def test_greedy(self):
        m = [
            [1, 1, 1, 1, 1],
            [1, 1, -1, 1, 1],
            [1, 1, -1, 1, 1],
            [20, 20, 20, 20, 1],
            [1, 1, 1, 1, 1],
        ]
        g = pathfind.transform.matrix2graph(m)

        f = pathfind.finder.Greedy()
        p = f.find(g, "4,0", "0,0")
        # g.show(trace=p)
        self.assertEqual(['4,0', '3,0', '2,0', '1,0', '0,0'], p)
