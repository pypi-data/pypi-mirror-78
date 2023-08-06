#!/usr/bin/env python3
#
# Copyright (C) 2019-2020 Cochise Ruhulessin
#
# This file is part of iam.ext.{{ pkg_name }}.
#
# iam.ext.{{ pkg_name }} is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# iam.ext.{{ pkg_name }} is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with iam.ext.{{ pkg_name }}.  If not, see <https://www.gnu.org/licenses/>.
import json
import os
import sys
from setuptools import find_namespace_packages
from setuptools import setup


version = str.strip(open('iam/ext/idc/VERSION').read())


setup(
    name='iam.ext.idc',
    version=version,
    packages=find_namespace_packages(),
    include_package_data=True,
    **json.loads((open('iam/ext/idc/package.json').read()))
)
