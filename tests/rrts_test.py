import random
import unittest

import pathfind


class RRTsTest(unittest.TestCase):

    def test_rrts1(self):
        m = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, -1, -1, 1, 1, -1, 1, 1],
            [1, 1, -1, 1, 1, -1, 1, 1],
            [1, 1, 1, 1, 1, -1, 1, 1],
        ]
        random.seed(2)
        g = pathfind.transform.matrix2graph(m, diagonal=True)
        f = pathfind.finder.RRTs()
        p = f.find(g, "4,0", "4,7")
        # print(p)
        # g.show(p)
        self.assertEqual([
            '4,0', '4,1', '3,1', '3,0', '2,0', '1,0', '0,1', '0,2', '0,3',
            '0,4', '0,5', '1,6', '2,7', '3,7', '4,7'], p)
