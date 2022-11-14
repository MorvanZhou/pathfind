import unittest

import pathfind


class DFSTest(unittest.TestCase):
    def test_dfs(self):
        m = [
            [1, 1, 1, 1, 1],
            [1, 1, -1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ]
        g = pathfind.transform.matrix2graph(m)

        alg = pathfind.finder.DeptFirstSearch()
        p = alg.find(g, "2,2", "0,2")
        # g.plot(trace=p)
        self.assertEqual([
            '2,2',
            '2,3',
            '2,4',
            '3,4',
            '4,4',
            '4,3',
            '4,2',
            '4,1',
            '4,0',
            '3,0',
            '2,0',
            '1,0',
            '1,1',
            '0,1',
            '0,2'], p)
