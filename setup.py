#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from setuptools import setup


if sys.version_info[0] < 3:
    sys.exit('Python < 3 is unsupported.')


setup(
    name='ippbxpy',
    version='2.0.3',
    author='Denis Gubanov',
    author_email='v12aml@gmail.com',
    py_modules=['ippbxpy'],
    scripts=['bin/ippbxpy'],
)


# EOF
