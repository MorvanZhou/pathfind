import unittest

import pathfind


class DijTest(unittest.TestCase):
    def test_dij(self):
        m = [
            [1, 1, 1, 1, 1],
            [1, 1, -1, 1, 1],
            [1, 1, -1, 1, 1],
            [20, 20, 20, 20, 1],
            [1, 1, 1, 1, 1],
        ]
        g = pathfind.transform.matrix2graph(m)

        f = pathfind.finder.Dijkstra()
        p = f.find(g, "4,0", "0,0")
        # g.show(trace=p)
        self.assertEqual(
            ['4,0', '4,1', '4,2', '4,3', '4,4', '3,4', '2,4', '1,4', '0,4', '0,3', '0,2', '0,1', '0,0'], p)
