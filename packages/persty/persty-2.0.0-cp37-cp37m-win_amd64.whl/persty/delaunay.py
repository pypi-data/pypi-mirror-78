import numpy as np
import persty.cpp.binding as _cpp

def edges(points):
    assert type(points) == np.ndarray, "points must be nd.array"
    assert len(points.shape) == 2, "points must have shape (n,d), with n number points and d their dimension"
    dimension = len(points[0])
    if dimension == 2:
        # sort points along x-axis
        sorted_indices1 = np.argsort(points[:,0])
        points1 = points[sorted_indices1]
        # get orizontal edges
        res1 = _cpp.horizontal_delaunay_edges_2D(points1)
        H_edges = sorted([tuple(sorted((sorted_indices1[i], sorted_indices1[j])))
                              for i, j in res1])

        # flip points and sort again
        points2 = np.empty(points.shape, dtype=points.dtype)
        points2[:,0] = np.copy(points[:,1])
        points2[:,1] = np.copy(points[:,0])
        sorted_indices2 = np.argsort(points2[:,0])
        points2 = points2[sorted_indices2]
        # get vertical edges
        res2 = _cpp.horizontal_delaunay_edges_2D(points2)
        V_edges = sorted([tuple(sorted((sorted_indices2[i], sorted_indices2[j])))
                              for i, j in res2])
        return sorted(H_edges + V_edges)
    else:
        print("only 2D array are valid")
        return None
