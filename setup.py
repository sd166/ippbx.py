#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from distutils.core import setup


if sys.version_info[0] < 3:
    sys.exit('Python < 3 is unsupported.')

setup(
    name='ippbx',
    version='2.0.3',
    author='Denis Gubanov',
    author_email='v12aml@gmail.com',
    py_modules=['ippbx'],
)


# EOF
