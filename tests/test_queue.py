import unittest

import pathfind
from pathfind.finder import queue


class QueueTest(unittest.TestCase):

    def test_fifo(self):
        fifo = queue.FifoFinderQueue()
        fifo.put(pathfind.Node(name="a"))
        fifo.put(pathfind.Node(name="b"))
        fifo.put(pathfind.Node(name="c"))
        self.assertEqual(fifo.get().name, "a")
        self.assertEqual(fifo.get().name, "b")
        self.assertFalse(fifo.empty())
        self.assertEqual(fifo.get().name, "c")
        self.assertTrue(fifo.empty())

    def test_filo(self):
        lifo = queue.LifoFinderQueue()
        lifo.put(pathfind.Node(name="a"))
        lifo.put(pathfind.Node(name="b"))
        lifo.put(pathfind.Node(name="c"))
        self.assertEqual(lifo.get().name, "c")
        self.assertEqual(lifo.get().name, "b")
        self.assertFalse(lifo.empty())
        self.assertEqual(lifo.get().name, "a")
        self.assertTrue(lifo.empty())

    def test_priority(self):
        q = queue.PriorityFinderQueue()
        q.put(pathfind.Node(name="a"), 1)
        q.put(pathfind.Node(name="b"), 2)
        q.put(pathfind.Node(name="c"), 0)
        self.assertEqual(q.get().name, "c")
        self.assertEqual(q.get().name, "a")
        self.assertFalse(q.empty())
        self.assertEqual(q.get().name, "b")
        self.assertTrue(q.empty())
