#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

import setuptools

from csv2googlesheets import __version__


# Package meta-data.
NAME = 'csv2googlesheets'
DESCRIPTION = 'Export data from CSV into Google sheets'
URL = 'https://github.com/alexskrn/csv2googlesheets'
EMAIL = 'alex.g.skrn@gmail.com'
AUTHOR = 'AlexSkrn'
REQUIRES_PYTHON = '>=3.6.0,<4.0.0'

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
try:
    with io.open(os.path.join(here, 'readme.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


def list_reqs(fname='requirements.txt'):
    """Return a list of packages required for this module to be executed."""
    with open(fname) as fd:
        return fd.read().splitlines()


setuptools.setup(
    name=NAME,
    version=__version__,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=setuptools.find_packages(exclude=('tests',)),
    install_requires=list_reqs(),
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='csv to Google sheets converter',
    entry_points={
        'console_scripts': [
            'csv2g=csv2googlesheets.to_google_sheets:main',
        ],
    },
)
