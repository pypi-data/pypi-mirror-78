from os import environ

__all__ = ['lti_dos']
__version__ = '20.9.0'


if environ.get('ASE_EXT') != 'disabled':
    from ase_ext.lti_dos import lti_dos
