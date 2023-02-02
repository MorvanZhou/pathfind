import unittest

import pathfind


class DijTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        m = [
            [1, 1, 1, 1, 1],
            [1, 2, pathfind.INFINITY, 1, 1],
            [1, 1, 1, 1, 1],
            [8, 3, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ]
        cls.g = pathfind.transform.matrix2graph(m)
        cls.dg = pathfind.transform.matrix2graph(m, diagonal=True)

    def test_k0(self):
        f = pathfind.finder.AStar(k=0)
        p = f.find(self.g, "4,0", "0,0")
        self.assertEqual(['4,0', '4,1', '3,1', '2,1', '2,0', '1,0', '0,0'], p)

    def test_large_k(self):
        f = pathfind.finder.AStar(k=100)
        p = f.find(self.g, "4,0", "0,0")
        self.assertEqual(['4,0', '3,0', '2,0', '1,0', '0,0'], p)

    def test_k1(self):
        f = pathfind.finder.AStar()
        p = f.find(self.g, "4,0", "0,0")
        self.assertEqual(['4,0', '4,1', '3,1', '2,1', '2,0', '1,0', '0,0'], p)
        # self.g.show(p)

    def test_diagonal(self):
        f = pathfind.finder.AStar()
        p = f.find(self.dg, "4,0", "0,0")
        # self.dg.show(p)
        self.assertEqual(['4,0', '4,1', '3,2', '2,1', '1,0', '0,0'], p)
