#!/usr/bin/env python

# pylint: disable=W0404,W0622,W0704,W0613,W0152
# copyright 2003-2020 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of logilab-pybill.
#
# logilab-pybill is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option) any
# later version.
#
# logilab-pybill is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with logilab-pybill.  If not, see <http://www.gnu.org/licenses/>.
"""Generic Setup script, takes package info from __pkginfo__.py file.
"""
__docformat__ = "restructuredtext en"

from setuptools import setup
from os import path

here = path.dirname(__file__)

pkginfo = {}
with open(path.join(here, "pybill", "__pkginfo__.py")) as f:
    exec(f.read(), pkginfo)

with open(path.join(here, "README"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=pkginfo["distname"],
    version=pkginfo["version"],
    description=pkginfo["description"],
    long_description=long_description,
    url=pkginfo["web"],
    author=pkginfo["author"],
    author_email=pkginfo["author_email"],
    install_requires=pkginfo["install_requires"],
    license=pkginfo["license"],
    classifiers=pkginfo["classifiers"],
    scripts=pkginfo["scripts"],
)
