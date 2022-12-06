import typing as tp

from pathfind.graph import Grid, INFINITY


def matrix2graph(matrix: tp.Sequence[tp.Sequence[float]], diagonal: bool = False) -> Grid:
    """
    Transform 2D matrix data to graph data. Data in matrix defines the cost for each cell. A cost < 0 indicates a road
     road to this cell is not connected.

    Args:
        matrix: 2D list for cost matrix
        diagonal (bool): include diagonal path, default to False

    Returns:
        Grid: graph data
    """
    g = Grid(has_diagonal=diagonal)

    for i, row in enumerate(matrix):
        dim2 = len(row)
        for j in range(dim2):
            w = row[j]
            if w is None or w < 0:
                w = INFINITY
            g.add_node_by_coord(i, j, w)

    return g
