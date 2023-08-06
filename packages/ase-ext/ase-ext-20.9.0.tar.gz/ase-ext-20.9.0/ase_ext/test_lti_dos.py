import numpy as np
from scipy.spatial import Delaunay
from ase.dft.dos import lti_dos
from ase.parallel import world


def test_lti_dos():
    indices = np.array([[i, j, k]
                        for i in [0, 1]
                        for j in [0, 1]
                        for k in [0, 1]])
    dt = Delaunay(np.dot(indices, np.eye(3)))
    simplices = indices[dt.simplices]

    eigs = np.zeros((2, 1, 13, 2))[:, :, 1:2]
    eigs[0, 0, 0, :] = 1

    weights = np.ones((2, 1, 1, 2, 2))
    weights[0, 0, 0, :, 1] = 0.5

    energies = np.linspace(-0.5, 1.5, 3)
    dos = np.empty((2, 3))

    lti_dos(simplices,
            eigs,
            weights,
            energies,
            dos,
            world)

    print(dos)

    assert np.allclose(dos, [[0, 4, 0], [0, 3, 0]])
