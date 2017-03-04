#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
from .ippbx import main


__author__ = 'Denis Gubanov'
__version__ = '2.0.3'

if sys.version_info[0] < 3:
    raise ImportError('Python < 3 is unsupported.')

main()


# EOF
