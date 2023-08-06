import numpy as np
import persty.util

def test_A_r1():
    p = np.array([0.0, 0.3, -0.2])
    q = np.array([1.0, 0.9, 0.2])
    A1 = persty.util.get_A_r(p,q)
    A2 = np.array([[0.5, 0.5], [0.4, 0.8], [-0.3, 0.3]])
    assert np.isclose(A1, A2).all()

def test_A_r2():
    p = np.array([0.0, 0.0, 0.0])
    q = np.array([1.0, 0.98, 1.0])
    A1 = persty.util.get_A_r(p,q)
    A2 = np.array([[0.5, 0.5], [0.48, 0.5], [0.5, 0.5]])
    assert np.isclose(A1, A2).all()
