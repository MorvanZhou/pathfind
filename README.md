# PathFind

Implementation of path finding algorithms including:

- Breadth-First Search (BFS)
- Dijkstra Search
- Greedy Best-First Search
- A\* Search

# Install

```shell
pip install pathfind
```

# Usage

Define a graph to transform graph from a matrix, then find a path from start point to end point.

```python
import pathfind

m = [
    [1, 1, 1, 1, 1],
    [1, 2, -1, 1, 1],
    [1, 1, 1, 1, 1],
    [8, 3, 1, 1, 1],
    [1, 1, 1, 1, 1],
]
graph = pathfind.transform.matrix2graph(m)
path = pathfind.find(graph, start="4,0", end="0,0")
# ['4,0', '4,1', '3,1', '2,1', '2,0', '1,0', '0,0']

graph.plot(trace=path)
```

<img src="https://raw.githubusercontent.com/MorvanZhou/pathfind/master/demo/astar.png" alt="drawing" width="250"/>


Finder can be changed by passing a string method ("a*", "bfs", "greedy", "dijkstra").

```python
path = pathfind.find(graph, start="4,0", end="0,0", method="bfs")
# ['2,2', '2,1', '1,1', '0,1', '0,2']

graph.plot(trace=path)
```

<img src="https://raw.githubusercontent.com/MorvanZhou/pathfind/master/demo/bfs.png" alt="drawing" width="250"/>


Set graph by hand.

```python
conf = [
    ["n1", "n2", 0.1],
    ["n1", "n3", 0.2],
    ["n2", "n3", 0.3]
]
graph = pathfind.Graph(conf)
graph.plot()
```

<img src="https://raw.githubusercontent.com/MorvanZhou/pathfind/master/demo/graph.png" alt="drawing" width="250"/>

Or you can set edge's and node's details by following way：

```python
n1 = pathfind.Node()
n2 = pathfind.Node()
n3 = pathfind.Node()
e1 = pathfind.Edge(node1=n1, node2=n2, weight=0.2)
e2 = pathfind.Edge(node1=n1, node2=n3, weight=0.1)
e3 = pathfind.Edge(n2, n3, weight=0)

g = pathfind.Graph()
g.add_edges([e1, e2, e3])
g.edges
"""
{'n0:n1': n0:n1, 'n0:n2': n0:n2, 'n1:n2': n1:n2}
"""
```

# More examples

More examples and usages can be found in [test](/tests)

