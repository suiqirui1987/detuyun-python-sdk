#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import sys
import detuyun

if sys.version_info <= (2, 5) or sys.version_info >= (2, 8):
    error = "ERROR: DetuYun SDK requires Python Version 2.6 or 2.7 ... exiting\n"
    sys.stderr.write(error)
    sys.exit(1)

setup(
    name='detuyun',
    version=detuyun.__version__,
    description='DetuYun Storage SDK for Python',
    license='',
    platforms='',
    author='',
    author_email='',
    url='',
    packages=['detuyun'],
    keywords=['detuyun', 'python', 'sdk'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)

try:
    import requests
except ImportError:
    msg = "\nOPTIONAL: pip install requests (recommend)\n"
    sys.stderr.write(msg)
