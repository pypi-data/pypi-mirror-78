#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Setup this SWIG library."""
import runpy

from setuptools import Extension, find_packages, setup
from setuptools.command.build_py import build_py

UAV_FDM_EXT = Extension(
    name='_uav_fdm',
    sources=[
        'uav_fdm.cpp',
        'uav_fdm_wrap.cxx',
        'gencode/sam_intercepter2/uav_fdm3d_ert_rtw/uav_fdm3d.cpp',
        'gencode/sam_intercepter2/uav_fdm3d_ert_rtw/uav_fdm3d_capi.cpp',
        'gencode/sam_intercepter2/uav_fdm3d_ert_rtw/uav_fdm3d_data.cpp'
    ],
    include_dirs=[
        'gencode/R2018b/rtw/c/src',
        'gencode/R2018b/rtw/c/src/ext_mode/common',
        'gencode/R2018b/rtw/c/src/common',
        'gencode/R2018b/simulink/include',
        'gencode/sam_intercepter2/uav_fdm3d_ert_rtw'
    ]
)

# Build extensions before python modules,
# or the generated SWIG python files will be missing.


class BuildPy(build_py):
    def run(self):
        self.run_command('build_ext')
        super().run()


INFO = runpy.run_path('_meta.py')

setup(
    name='uav-fdm',
    description='A UAV FDM model for sim',
    version=INFO['__version__'],
    author=INFO['__author__'],
    license=INFO['__copyright__'],
    author_email=INFO['__email__'],
    url=INFO['__url__'],
    keywords=['uav', 'fdm'],

    # packages=find_packages('.'),
    #package_dir={'': '.'},
    py_modules=['uav_fdm','_meta'],
    ext_modules=[UAV_FDM_EXT],
    cmdclass={
        'build_py': BuildPy,
    },
    include_package_data=True,

    python_requires='>=3.4',
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
