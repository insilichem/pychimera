#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from setuptools import setup, find_packages
import os

import pychimera

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='pychimera',
    version=pychimera.__version__,
    url='https://github.com/insilichem/pychimera',
    download_url='https://github.com/insilichem/pychimera/tarball/{}'.format(
        pychimera.__version__),
    license='LGPL',
    author=pychimera.__author__,
    author_email='jaime.rogue@gmail.com',
    description=pychimera.__doc__.splitlines()[4],
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Chemistry',
    ],
    scripts=['pychimera']
)
