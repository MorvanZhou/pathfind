import unittest

import pathfind


class DFSTest(unittest.TestCase):
    def test_dfs(self):
        m = [
            [1, 1, 1, 1, 1],
            [1, 1, pathfind.INFINITY, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ]
        g = pathfind.transform.matrix2graph(m)

        f = pathfind.finder.DepthFirstSearch()
        p = f.find(g, "2,2", "0,2")
        # g.show(trace=p)
        self.assertEqual(['2,2', '3,2', '4,2', '4,3', '4,4', '3,4', '2,4', '1,4', '1,3', '0,3', '0,2'], p)
