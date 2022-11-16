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
        path = ["A", "B", "C", "G"]
        start = path[0]
        alg = pathfind.finder.DStarLite()
        i = 1
        real_path = [start]
        while True:
            start = next(alg.explore(self.g, start, "G"))
            if start is None:
                break
            real_path.append(start)
            self.assertEqual(path[i], start)
            i += 1
        self.assertEqual(["A", "B", "C", "G"], real_path)
        # self.g.plot(real_path)

    def test_change_weight(self):
        path = ["A", "B", "D", "G"]
        start = path[0]
        alg = pathfind.finder.DStarLite()
        i = 1
        real_path = [start]
        while True:
            start = next(alg.explore(self.g, start, "G"))
            if start is None:
                break
            real_path.append(start)
            self.assertEqual(path[i], start)
            i += 1
            if i == 2:
                self.g.edges["C:G"].set_weight(float("inf"), float("inf"))
                self.g.edges["B:C"].set_weight(float("inf"), float("inf"))

        self.assertEqual(path, real_path)
        # self.g.plot(real_path)

    def test_find(self):
        alg = pathfind.finder.DStarLite()
        path = alg.find(self.g, "A", "G")
        self.assertEqual(["A", "B", "C", "G"], path)

        path = alg.find(self.g, "B", "G")
        self.assertEqual(["B", "C", "G"], path)
