#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import ippbx
from distutils.core import setup


if sys.version_info[0] < 3:
    sys.exit('Python < 3 is unsupported.')

setup(
    name='ippbx',
    version=ippbx.__version__,
    py_modules=['ippbx'],
)


# EOF
