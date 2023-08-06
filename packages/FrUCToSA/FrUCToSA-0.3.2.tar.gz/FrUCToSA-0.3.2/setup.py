#!/bin/env python

#######################################################################
# Copyright (C) 2020 David Palao
#
# This file is part of FrUCToSA.
#
#  FrUCToSA is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  FrUCToSA is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with FrUCToSA.  If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################

import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


install_requirements = ["psutil"]


setup(
    name="FrUCToSA",
    version='0.3.2',
    description="A package to collect and analyze basic performance data from clusters",
    long_description=long_description,
    author="David Palao",
    author_email="palao@csc.uni-frankfurt.de",
    url="https://itp.uni-frankfurt.de/~palao/software/FrUCToSA",
    python_requires=">=3.7",
    license='GNU General Public License (GPLv3)',
    packages=find_packages(),
    provides=["fructosa"],
    install_requires=install_requirements,
    platforms=['GNU/Linux'],
    entry_points={'console_scripts': [
        "fructosad = fructosa.fructosad:main",
        "lagent = fructosa.lagent:main",
        "lmaster = fructosa.lmaster:main",
        "make-fructosa-dashboard = fructosa.grafana.dashboard:make_dashboard",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: No Input/Output (Daemon)",
        "Framework :: AsyncIO",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: System :: Monitoring",
    ],
    #test_suite="tests",
)
