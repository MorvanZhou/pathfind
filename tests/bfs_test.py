import unittest

import pathfind


class BFSTest(unittest.TestCase):
    def test_bfs(self):
        m = [
            [1, 1, 1, 1, 1],
            [1, 1, -1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ]
        g = pathfind.transform.matrix2graph(m)

        alg = pathfind.finder.BreadthFirstSearch()
        p = alg.find(g, "2,2", "0,2")
        # g.plot(trace=p)
        self.assertEqual(['2,2', '2,1', '1,1', '0,1', '0,2'], p)
