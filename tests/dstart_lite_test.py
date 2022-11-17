import unittest

import pathfind


class DStarLiteTest(unittest.TestCase):
    def setUp(self) -> None:
        self.g = pathfind.Graph(conf=[
            ["A", "B", 1, 1, (0, 0), (0, 1)],
            ["B", "C", 1, 1, (0, 1), (0, 2)],
            ["B", "D", 1, 1, (0, 1), (1, 1)],
            # ["C", "D", 1, 1, (0, 2), ()],
            ["C", "G", 1, 1, (0, 2), (2, 1)],
            ["D", "G", 10, 10, (1, 1), (2, 1)],
        ])

    def test_no_change(self):
        expected_path = ["A", "B", "C", "G"]
        start = expected_path[0]
        f = pathfind.finder.DStarLite()
        e = f.iter_explore(self.g, start, "G")
        i = 0
        while True:
            new_g = next(e)
            if new_g is None:
                break
            if i == 0:
                self.assertEqual({'G': 0.0, 'C': 1.0, 'A': 3.0, 'B': 2.0, 'D': pathfind.INFINITY}, new_g)
            else:
                self.assertEqual({}, new_g)
            i += 1
        p = f.traceback(f.came_from)
        self.assertEqual(expected_path, p)
        # self.g.plot(p)

    def test_change_weight(self):
        expected_path = ["A", "B", "D", "G"]
        start = expected_path[0]
        f = pathfind.finder.DStarLite()
        e = f.iter_explore(self.g, start, "G")
        i = 0
        while True:
            if i == 1:
                self.g.edges["C:G"].set_weight(float("inf"), 10)
                self.g.edges["B:C"].set_weight(float("inf"), 10)
            new_g = next(e)
            if new_g is None:
                break
            if i == 0:
                self.assertEqual({'G': 0.0, 'C': 1.0, 'A': 3.0, 'B': 2.0, 'D': pathfind.INFINITY}, new_g)
            elif i == 1:
                self.assertEqual({'D': 10.0, 'A': pathfind.INFINITY, 'B': 11.0}, new_g)
            else:
                self.assertEqual({}, new_g)
            i += 1

        p = f.traceback(f.came_from)
        self.assertEqual(expected_path, p)
        # self.g.plot(p)

    def test_find(self):
        f = pathfind.finder.DStarLite()
        path = f.find(self.g, "A", "G")
        self.assertEqual(["A", "B", "C", "G"], path)

        path = f.find(self.g, "B", "G")
        self.assertEqual(["B", "C", "G"], path)
