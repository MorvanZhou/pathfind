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
    finder: BaseFinder = METHOD_MAP[method.lower()]()
    return finder.find(graph, start, end)
