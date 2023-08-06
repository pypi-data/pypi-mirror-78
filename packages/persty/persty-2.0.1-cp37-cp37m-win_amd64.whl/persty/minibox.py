import persty.cpp.binding as _cpp
import numpy as np

def edges(points):
    """
    Minibox edges of d-dimensional points.

    Parameters
    ----------
    points: (n,d) numpy array

    Return
    ------
    edges: list of tuples
        Pairs of indices of `points` representing
        their Minibox edges.
    """
    assert type(points) == np.ndarray, "points must be nd.array"
    assert len(points.shape) == 2, "points must have shape (n,d), with n number points and d their dimension"
    dimension = len(points[0])
    if dimension == 2:
        sorted_indices = np.argsort(points[:,0])
        points = points[sorted_indices]
        res = _cpp.minibox_edges_2D(points)
        return sorted([tuple(sorted((sorted_indices[i], sorted_indices[j]))) for i, j in res])
    elif dimension == 3:
        sorted_indices = np.argsort(points[:,0])
        points = points[sorted_indices]
        res = _cpp.minibox_edges_3D(points)
        return sorted([tuple(sorted((sorted_indices[i], sorted_indices[j]))) for i, j in res])
    elif dimension > 3:
        return _cpp.brute_minibox_edges(points)

def edges_n_dim(points):
    """
    Minibox edges of d-dimensional points.

    Parameters
    ----------
    points: (n,d) numpy array

    Return
    ------
    edges: list of tuples
        Pairs of indices of `points` representing
        their Minibox edges.
    """

    return _cpp.brute_minibox_edges(points)
