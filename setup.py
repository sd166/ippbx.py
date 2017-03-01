#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from distutils.core import setup


if sys.version_info[0] < 3:
    sys.exit('Python < 3 is unsupported.')

setup(
    name='ippbx',
    version='2.0.3',
    py_modules=['ippbx'],
)


# EOF
