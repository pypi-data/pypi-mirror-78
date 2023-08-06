# copyright 2003-2020 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of logilab-doctools.
#
# logilab-doctools is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option) any
# later version.
#
# logilab-doctools is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with logilab-doctools.  If not, see <http://www.gnu.org/licenses/>.
"""PyBill packaging information"""
__docformat__ = "restructuredtext en"

from os.path import join

distname = "pybill"
modname = "pybill"
debian_name = "pybill"

numversion = (1, 2, 0)
version = ".".join([str(num) for num in numversion])
pyversions = ["3.6"]

license = "LGPL"
description = "PDF formatting tool for bills"
mailinglist = "mailto://python-projects@lists.logilab.org"
web = "http://www.logilab.org/project/%s" % distname
author = "Olivier Cayrol"
author_email = "olivier.cayrol@logilab.fr"

# executable (include the 'bin' directory in the name)

scripts = [join("bin", name) for name in ("pybill",)]

install_requires = [
    "setuptools",
    "reportlab == 3.5.42",
    "docutils",
    "lxml",
    "logilab-common",
]


classifiers = [
    "Topic :: Utilities",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3 :: Only",
]
