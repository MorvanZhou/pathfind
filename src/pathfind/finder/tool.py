from pathfind.graph.graph import Graph
from pathfind.finder import alg
from pathfind.finder.finder import BaseFinder, GraphPath

METHOD_MAP = {
    "a*": alg.AStar,
    "bfs": alg.BFS,
    "greedy": alg.Greedy,
    "dijkstra": alg.Dijkstra,
}


def find(graph: Graph, start: str, end: str, method="a*") -> GraphPath:
    finder: BaseFinder = METHOD_MAP[method.lower()]()
    return finder.find(graph, start, end)
