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
        # g.show(trace=p)
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
        f = pathfind.finder.AStar()
        p = f.find(g, "4,0", "0,0")
        self.assertEqual(['4,0', '4,1', '3,1', '2,1', '2,0', '1,0', '0,0'], p)

    def test_iter_explore(self):
        m = [
            [1, 1, 1, 1, 1],
            [1, 2, -1, 1, 1],
            [1, 1, 1, 1, 1],
            [8, 3, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ]
        g = pathfind.transform.matrix2graph(m)
        f = pathfind.finder.AStar()
        get_cost = f.iter_explore(graph=g, start="4,0", end="0,0")
        self.assertEqual({'4,0': 0, '3,0': 4.5, '4,1': 1.0}, next(get_cost))

        self.assertEqual({'3,1': 3.0, '4,2': 2.0}, next(get_cost))
        self.assertEqual({'2,1': 5.0, '3,2': 5.0}, next(get_cost))

    def test_next_explore(self):
        m = [
            [1, 1, 1, 1, 1],
            [1, 2, -1, 1, 1],
            [1, 1, 1, 1, 1],
            [8, 3, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ]
        g = pathfind.transform.matrix2graph(m)
        f = pathfind.finder.AStar()
        n = f.next(graph=g, start="4,0", end="0,0")
        self.assertEqual("4,1", n)
        n = f.next(graph=g, start=n, end="0,0")
        self.assertEqual("3,1", n)
        n = f.next(graph=g, start=n, end="0,0")
        self.assertEqual("2,1", n)
        n = f.next(graph=g, start=n, end="0,0")
        self.assertEqual("2,0", n)
        n = f.next(graph=g, start=n, end="0,0")
        self.assertEqual("1,0", n)
        n = f.next(graph=g, start=n, end="0,0")
        self.assertEqual("0,0", n)
        n = f.next(graph=g, start=n, end="0,0")
        self.assertEqual("0,0", n)

    def test_start_at_infinity(self):
        m = [
            [1, -1, 1, 1, 1],
            [-1, -1, -1, 1, 1],
            [1, 1, 1, 1, 1],
            [8, 3, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ]
        g = pathfind.transform.matrix2graph(m)
        for c in pathfind.finder.alg.METHOD_MAP.values():
            f = c()
            path = f.find(g, "0,1", "4,0")
            self.assertEqual(0, len(path))

    def test_no_path(self):
        m = [
            [1, -1, 1, 1, 1],
            [-1, -1, -1, 1, 1],
            [1, 1, 1, 1, 1],
            [8, 3, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ]
        g = pathfind.transform.matrix2graph(m)
        for c in pathfind.finder.alg.METHOD_MAP.values():
            f = c()
            path = f.find(g, "0,0", "4,0")
            self.assertEqual(0, len(path))
