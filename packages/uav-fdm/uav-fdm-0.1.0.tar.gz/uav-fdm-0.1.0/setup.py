#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Setup this SWIG library."""
import runpy

from setuptools import Extension, find_packages, setup
from setuptools.command.build_py import build_py

UAV_FDM_EXT = Extension(
    name='_uav_fdm',
    swig_opts=['-c++'],
    sources=[
        'uav_fdm.cpp',
        'uav_fdm.i',
    ]
)

# Build extensions before python modules,
# or the generated SWIG python files will be missing.
class BuildPy(build_py):
    def run(self):
        self.run_command('build_ext')
        super(build_py, self).run()


INFO = runpy.run_path('_meta.py')

setup(
    name='uav-fdm',
    description='A UAV FDM model for sim',
    version=INFO['__version__'],
    author=INFO['__author__'],
    license=INFO['__copyright__'],
    author_email=INFO['__email__'],
    url=INFO['__url__'],
    keywords=['SWIG', 'uav', 'fdm'],

    #packages=find_packages('.'),
    #package_dir={'': '.'},
    py_modules=['uav_fdm'],
    ext_modules=[UAV_FDM_EXT],
    cmdclass={
        'build_py': BuildPy,
    },

    python_requires='>=3.4',
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
       