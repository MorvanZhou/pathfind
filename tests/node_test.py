import unittest

import pathfind
from pathfind.graph.node import _reset_global_name_count


class NodeTest(unittest.TestCase):

    def test_name(self):
        _reset_global_name_count()
        self.assertEqual("n0", pathfind.Node().name)
        self.assertEqual("a", pathfind.Node(name="a").name)
        self.assertEqual("n1", pathfind.Node().name)
