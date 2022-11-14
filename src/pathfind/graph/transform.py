import typing as tp

from pathfind.graph import Graph, Edge, Node


def matrix2graph(matrix: tp.Sequence[tp.Sequence[float]]) -> Graph:
    """
    Transform 2D matrix data to graph data. Data in matrix defines the cost for each cell. A cost < 0 indicates a road
     road to this cell is not connected.

    Args:
        matrix: 3D cost matrix

    Returns:
        Graph: graph data
    """
    n_dict = {}

    def get_node(i, j):
        name = f"{i},{j}"
        if name in n_dict:
            n = n_dict[name]
        else:
            n = Node(name, position=(i, j))
            n_dict[name] = n
        return n

    def add_edge(cell_pos, next_pos):
        cell_weight = matrix[cell_pos[0]][cell_pos[1]]
        next_weight = matrix[next_pos[0]][next_pos[1]]
        if cell_weight < 0 or next_weight < 0:  # is not connected
            return
        weight = (cell_weight + next_weight) / 2
        g.add_edge(Edge(
            get_node(*cell_pos),
            get_node(*next_pos),
            weight
        ))

    g = Graph()

    dim1 = len(matrix)
    for i, row in enumerate(matrix):
        dim2 = len(row)
        for j in range(dim2):
            if i < dim1 - 1:
                # has bottom cell
                add_edge((i, j), (i + 1, j))

            if j < dim2 - 1:
                # has right cell
                add_edge((i, j), (i, j + 1))
    return g
