import typing as tp

from pathfind.finder.alg.a_star import AStar
from pathfind.finder.alg.breadth_first_search import BreadthFirstSearch, BFS
from pathfind.finder.alg.d_star_lite import DStarLite
from pathfind.finder.alg.depth_first_search import DepthFirstSearch, DFS
from pathfind.finder.alg.dijkstra import Dijkstra
from pathfind.finder.alg.greedy_best_first import GreedyBestFirst, Greedy
from pathfind.finder.alg.jump_point_search import JumpPointSearch, JPS
from pathfind.finder.finder import BaseFinder, GraphPath
from pathfind.graph import Graph

METHOD_MAP: tp.Dict[str, tp.Callable] = {
    "a*": AStar,
    "bfs": BFS,
    "greedy": Greedy,
    "dijkstra": Dijkstra,
    "dfs": DFS,
    "d*lite": DStarLite,
    "jps": JPS,
}


def find(graph: Graph, start: str, end: str, method="a*") -> GraphPath:
    """Explore the graph from start point, get a traceback dictionary at the end.

    Args:
        graph (Graph): graph
        start (str): start node's name
        end (str): end node's name
        method (str): method name

    Returns:
        NodeTrace: a dictionary with key of node's name and value of :class:`~Node`, this is used for traceback
    """
    finder: BaseFinder = METHOD_MAP[method.lower()]()
    return finder.find(graph, start, end)


def next_move(graph: Graph, start: str, end: str, method="a*") -> str:
    """
    Next point to move on. This will compute complete path from start to end, then take the next point from start.

    Args:
        graph (Graph): graph
        start (str): start node's name
        end (str): end node's name
        method (str): method name

    Returns:
        str: next node's name
    """
    finder: BaseFinder = METHOD_MAP[method.lower()]()
    return finder.next(graph, start, end)
