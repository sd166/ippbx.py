#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os.path
from setuptools import setup, find_packages
# import ippbxpy


if sys.version_info[0] < 3:
    sys.exit('Python < 3 is unsupported.')


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='ippbxpy',
    # version=ippbxpy.__version__,
    version='2.0.3',
    author='Denis Gubanov',
    author_email='v12aml@gmail.com',
    # packages=find_packages(exclude=['tests']),
    packages=["ippbxpy"],
    long_description=read('README.md'),
    entry_points={
        "console_scripts": [
            "ippbxpy = ippbxpy.ippbx:main",
        ],
     },
)


# EOF
