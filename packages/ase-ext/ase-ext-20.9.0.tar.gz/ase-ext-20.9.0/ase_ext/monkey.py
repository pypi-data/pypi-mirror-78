import ase.dft.dos as dos
from ase_ext.lti_dos import lti_dos


def monkey_patch_ase():
    dos.lti_dos = lti_dos
