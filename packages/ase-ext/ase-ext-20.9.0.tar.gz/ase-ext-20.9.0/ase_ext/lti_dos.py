from numpy import ascontiguousarray as aca
from _ase_ext import lib
from ase_ext.utils import doublep, longp


def lti_dos(simplices, eigs, weights, energies, dos, world):
    simplices = aca(simplices)
    eigs = aca(eigs)
    weights = aca(weights)
    energies = aca(energies)
    cdos = aca(dos)
    cdos[:] = 0.0
    lib.lti_dos(longp(simplices),
                doublep(eigs),
                doublep(weights),
                doublep(energies),
                doublep(cdos),
                *weights.shape,
                len(energies),
                world.rank, world.size)
    cdos /= 6.0
    world.sum(cdos)
    if dos is not cdos:
        dos[:] = cdos
