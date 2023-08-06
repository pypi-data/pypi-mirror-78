import persty.cpp.binding as _cpp
import numpy as np
from itertools import combinations
from scipy.spatial.distance import chebyshev
from gudhi import SimplexTree

def get_minibox(p, q):
    """Minimal enclosing box of p and q."""
    assert type(p) == np.ndarray, "p must be nd.array"
    assert type(q) == np.ndarray, "q must be nd.array"
    assert p.shape == q.shape, "p and q must have same shape"
    return _cpp.get_minibox(p, q)

def is_inside(p, box):
    """Check if p is contained in the interior of box."""
    assert type(p) == np.ndarray, "p must be nd.array"
    assert type(box) == np.ndarray, "box must be nd.array"
    assert len(p) == len(box), "p and box must have same length"
    assert box.shape == (len(box), 2), "elements of box must have length equal to 2"
    return _cpp.is_inside(p, box)

def get_A_r(p, q):
    """Return the (d-1)-dimensional box defined by the
    intersection of the hypercubes of radius equal to
    half the Chebyshev distance between p and q and
    centered in these points.
    """
    assert type(p) == np.ndarray, "p must be nd.array"
    assert type(q) == np.ndarray, "q must be nd.array"
    assert p.shape == q.shape, "p and q must have same shape"
    return _cpp.get_A_r(p, q)

def clique_triangles(edges, number_points, dimension=2):
    """Return the clique triangles on `edges`

    Parameters
    ----------
    edges: list pairs of indices, list of list of int
        The edges of a graph built on some finite set of points
    number_points: int
        The number of vertices of the graph to which the edges belong
    dimension: int >=2
        Dimension of clique simplices returned

    Return
    ------
    clique_triangles: list of list of int
        The clique triangles on the given edges

    """

    dict_graph = {i: list() for i in range(number_points)}
    for i, j in edges:
        dict_graph[i].append(j)
        dict_graph[j].append(i)
    dict_graph = {key: set(value) for key, value in dict_graph.items()}

    triangles = set()
    for i, j in edges:
        for el in dict_graph[i]:
            if el in dict_graph[j]:
                triangles.add(tuple(sorted([i, j, el])))
    return list(triangles)

def make_gudhi_simplex_tree(points, edges, max_simplex_dim=2, metric=chebyshev):
    """Returns the `gudhi.SimplexTree()` object containing
    all simplices up to dimension `max_sim_dim`

    Parameters
    ----------
    points: list of list of floats
    """
    sim_tree = SimplexTree()
    vertices = list(range(len(points)))
    for v in vertices:
        sim_tree.insert(simplex=[v], filtration=0.0)
    for e in edges:
        p, q = points[e[0]], points[e[1]]
        sim_tree.insert(simplex=e, filtration=metric(p, q))
    sim_tree.expansion(max_simplex_dim)

    return sim_tree
