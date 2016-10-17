#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import os
import versioneer

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = versioneer.get_version()
setup(
    name='pychimera',
    version=version,
    cmdclass=versioneer.get_cmdclass(),
    url='https://github.com/insilichem/pychimera',
    download_url='https://github.com/insilichem/pychimera/tarball/v' + version,
    license='LGPL',
    author="Jaime Rodríguez-Guerra",
    author_email='jaime.rogue@gmail.com',
    description='Use UCSF Chimera Python API in a standard Python 2.7 interpreter.',
    long_description=read('README.rst'),
    packages=['pychimera'],
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
    scripts=['scripts/pychimera']
)
