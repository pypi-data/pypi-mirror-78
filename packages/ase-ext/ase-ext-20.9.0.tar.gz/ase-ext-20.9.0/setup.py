#!/usr/bin/env python3
import re
import sys
from setuptools import setup, find_packages, Extension
from pathlib import Path


if sys.version_info < (3, 6, 0, 'final', 0):
    raise SystemExit('Python 3.6 or later is required!')


with open('README.rst') as fd:
    long_description = fd.read()

# Get the current version number:
with open('ase_ext/__init__.py') as fd:
    version = re.search("__version__ = '(.*)'", fd.read()).group(1)


setup(name='ase-ext',
      version=version,
      description='C-extensions for the Atomic Simulation Environment',
      url='https://gitlab.com/ase/ase_ext',
      maintainer='ASE-community',
      maintainer_email='ase-users@listserv.fysik.dtu.dk',
      license='LGPLv2.1+',
      platforms=['unix'],
      packages=find_packages(),
      install_requires=['cffi'],
      ext_modules=[Extension('_ase_ext',
                             [str(path) for path in Path('c').glob('*.c')],
                             extra_compile_args=['-std=c99'])],
      long_description=long_description,
      classifiers=[
          'Development Status :: 6 - Mature',
          'License :: OSI Approved :: '
          'GNU Lesser General Public License v2 or later (LGPLv2+)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Scientific/Engineering :: Physics'])
