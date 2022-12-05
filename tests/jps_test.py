import unittest

import pathfind


class JPSTest(unittest.TestCase):

    def test_jps1(self):
        m = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, -1, 1, 1],
            [1, 1, 1, 1, 1, -1, 1, 1],
            [1, 1, 1, 1, 1, -1, 1, 1],
        ]
        g = pathfind.transform.matrix2graph(m, diagonal=True)
        f = pathfind.finder.JPS()
        p = f.find(g, "4,0", "4,7")
        # g.plot(p)
        # print(p)
        self.assertEqual(['4,0', '3,1', '2,2', '1,3', '1,4', '1,5', '2,6', '3,7', '4,7'], p)

    def test_jps2(self):
        m = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, -1, 1, 1, 1],
            [1, 1, -1, 1, 1, -1, 1, 1],
            [1, 1, 1, 1, 1, -1, 1, 1],
            [1, 1, 1, 1, 1, -1, 1, 1],
        ]
        g = pathfind.transform.matrix2graph(m, diagonal=True)
        f = pathfind.finder.JPS()
        p = f.find(g, "4,0", "4,7")
        # g.plot(p)
        # print(p)
        self.assertEqual(['4,0', '3,1', '3,2', '2,3', '2,4', '1,5', '2,6', '3,7', '4,7'], p)

    def test_jps3(self):
        m = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, -1, -1, 1, 1],
            [1, 1, -1, 1, 1, -1, 1, 1],
            [1, 1, 1, 1, 1, -1, 1, 1],
            [1, 1, 1, 1, 1, -1, 1, 1],
        ]
        g = pathfind.transform.matrix2graph(m, diagonal=True)
        f = pathfind.finder.JPS()
        p = f.find(g, "4,0", "4,7")
        # g.plot(p)
        # print(p)
        self.assertEqual(['4,0', '3,1', '3,2', '2,3', '1,3', '0,4', '0,5', '1,6', '2,7', '3,7', '4,7'], p)

    def test_jps_non_diagonal_map(self):
        m = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, -1, 1, 1, 1],
            [1, 1, -1, 1, 1, -1, 1, 1],
            [1, 1, 1, 1, 1, -1, 1, 1],
            [1, 1, 1, 1, 1, -1, 1, 1],
        ]
        g = pathfind.transform.matrix2graph(m, diagonal=False)
        f = pathfind.finder.JPS()
        with self.assertRaises(ValueError):
            _ = f.find(g, "4,0", "4,7")
