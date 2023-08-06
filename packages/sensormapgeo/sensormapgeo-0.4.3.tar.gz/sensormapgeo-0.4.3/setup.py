#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sensormapgeo, A package for transforming remote sensing images between sensor and map geometry.
#
# Copyright (C) 2020  Daniel Scheffler (GFZ Potsdam, danschef@gfz-potsdam.de)
#
# This software was developed within the context of the EnMAP project supported
# by the DLR Space Administration with funds of the German Federal Ministry of
# Economic Affairs and Energy (on the basis of a decision by the German Bundestag:
# 50 EE 1529) and contributions from DLR, GFZ and OHB System AG.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

version = {}
with open("sensormapgeo/version.py") as version_file:
    exec(version_file.read(), version)

requirements = ['numpy', 'gdal', 'pyresample>=1.11.0', 'py_tools_ds>=0.14.26', 'pyproj>=2.2']

setup_requirements = []

test_requirements = ['coverage', 'nose', 'nose-htmloutput', 'rednose']

setup(
    author="Daniel Scheffler",
    author_email='daniel.scheffler@gfz-potsdam.de',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A package for transforming remote sensing images between sensor and map geometry.",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='sensormapgeo',
    name='sensormapgeo',
    packages=find_packages(exclude=['tests*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitext.gfz-potsdam.de/EnMAP/sensormapgeo',
    version=version['__version__'],
    zip_safe=False,
)
