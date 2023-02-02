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
        # print(p)
        self.assertEqual(['4,0', '3,1', '3,2', '2,3', '1,3', '0,4', '0,5', '1,6', '2,7', '3,7', '4,7'], p)

    def test_jps_orthogonal(self):
        m = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, -1, 1, 1, 1],
            [1, 1, -1, 1, 1, -1, 1, 1],
            [1, 1, 1, 1, 1, -1, 1, 1],
            [1, 1, 1, 1, 1, -1, 1, 1],
        ]
        g = pathfind.transform.matrix2graph(m, diagonal=False)
        f = pathfind.finder.JPS()
        p = f.find(g, "4,0", "4,7")
        # g.show(p)
        self.assertEqual(
            ['4,0', '3,0', '2,0', '1,0', '0,0', '0,1', '0,2',
             '0,3', '0,4', '0,5', '1,5', '1,6', '2,6', '3,6', '4,6', '4,7'], p)

    def test_jps_orthogonal2(self):
        m = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, -1, 1, 1, 1],
            [1, 1, -1, 1, 1, 1, 1, 1],
            [1, 1, -1, 1, 1, -1, 1, 1],
            [1, 1, 1, 1, 1, -1, 1, 1],
        ]
        g = pathfind.transform.matrix2graph(m, diagonal=False)
        f = pathfind.finder.JPS()
        p = f.find(g, "4,0", "4,7")
        # g.show(p)
        self.assertEqual(
            ['4,0', '4,1', '4,2', '4,3', '3,3', '2,3', '2,4', '2,5', '2,6', '3,6', '4,6', '4,7'], p)

    def test_jps_orthogonal3(self):
        m = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, -1, 1, 1, 1],
            [1, 1, -1, 1, 1, 1, 1, 1],
            [1, 1, -1, 1, 1, -1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ]
        g = pathfind.transform.matrix2graph(m, diagonal=False)
        f = pathfind.finder.JPS()
        p = f.find(g, "4,0", "4,7")
        # g.show(p)
        self.assertEqual(
            ['4,0', '4,1', '4,2', '4,3', '4,4', '4,5', '4,6', '4,7'], p)
