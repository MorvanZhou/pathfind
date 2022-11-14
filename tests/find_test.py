import unittest

import pathfind


class FindTest(unittest.TestCase):
    def test_name_error(self):
        with self.assertRaises(KeyError):
            pathfind.find(pathfind.graph.Graph(), "2,2", "0,2", "xxx")

    def test_bfs(self):
        m = [
            [1, 1, 1, 1, 1],
            [1, 1, -1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ]
        g = pathfind.transform.matrix2graph(m)

        p = pathfind.find(g, "2,2", "0,2", "bfs")
        g.plot(trace=p)
        self.assertEqual(['2,2', '2,1', '1,1', '0,1', '0,2'], p)

    def test_astar(self):
        m = [
            [1, 1, 1, 1, 1],
            [1, 2, -1, 1, 1],
            [1, 1, 1, 1, 1],
            [8, 3, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ]
        g = pathfind.transform.matrix2graph(m)
        alg = pathfind.finder.AStar()
        p = alg.find(g, "4,0", "0,0")
        self.assertEqual(['4,0', '4,1', '3,1', '2,1', '2,0', '1,0', '0,0'], p)
