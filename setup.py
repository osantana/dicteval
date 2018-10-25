#!/usr/bin/env python

import io
import os

from setuptools import find_packages, setup

NAME = 'dicteval'
DESCRIPTION = 'Evaluate expressions in dict/json objects'
URL = 'https://github.com/osantana/dicteval'
EMAIL = 'dicteval@osantana.me'
AUTHOR = 'Osvaldo Santana Neto'
REQUIRES_PYTHON = '>=3.7.0'
VERSION = "0.0.6"

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    install_requires=[],
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
