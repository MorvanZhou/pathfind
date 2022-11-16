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

    def test_k0(self):
        alg = pathfind.finder.AStar(k=0)
        p = alg.find(self.g, "4,0", "0,0")
        self.assertEqual(['4,0', '4,1', '3,1', '2,1', '2,0', '1,0', '0,0'], p)

    def test_large_k(self):
        alg = pathfind.finder.AStar(k=100)
        p = alg.find(self.g, "4,0", "0,0")
        self.assertEqual(['4,0', '3,0', '2,0', '1,0', '0,0'], p)

    def test_k1(self):
        alg = pathfind.finder.AStar()
        p = alg.find(self.g, "4,0", "0,0")
        self.assertEqual(['4,0', '4,1', '3,1', '2,1', '2,0', '1,0', '0,0'], p)
        # self.g.plot(p)
