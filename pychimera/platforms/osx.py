#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from .linux import (_patch_envvars as _patch_envvars_linux, 
                    launch_ipython)


CHIMERA_BINARY = 'chimera'
CHIMERA_PREFIX = 'Chimera*/Contents/Resources'
CHIMERA_LOCATIONS = ('/Applications', 
                     os.path.expanduser('~/.local'),
                     os.path.expanduser('~/Desktop'))
NULL = os.devnull

def _patch_envvars(basedir, libdir, nogui=True):
    _patch_envvars_linux(basedir, libdir, nogui)
    os.environ['FONTCONFIG_FILE'] = '/usr/X11/lib/X11/fonts/fonts.conf'
    sys.executable = os.path.join(basedir, 'bin', 'python2.7')


def _patch_paths(basedir, libdir, nogui=True):
    os.environ['PYTHONPATH'] = ':'.join(
        [os.path.join(basedir, 'share'),
         os.path.join(basedir, 'bin'),
         os.path.join(libdir, 'python27.zip'),
         os.path.join(libdir, 'python2.7'),
         os.path.join(libdir, 'python2.7', 'plat-darwin'),
         os.path.join(libdir, 'python2.7', 'plat-mac'),
         os.path.join(libdir, 'python2.7', 'plat-mac', 'lib-scriptpackages'),
         os.path.join(libdir, 'python2.7', 'lib-tk'),
         os.path.join(libdir, 'python2.7', 'lib-old'),
         os.path.join(libdir, 'python2.7', 'lib-dynload'),
         os.path.join(libdir, 'python2.7', 'site-packages')]
         + sys.path
         )


def _patch_libraries(basedir, libdir, nogui=True):
    try:
        OLD_FALLBACK_LIB = os.environ['DYLD_FALLBACK_LIBRARY_PATH']
    except KeyError:
        os.environ['DYLD_FALLBACK_LIBRARY_PATH'] = libdir
    else:
        os.environ['CHIMERA_DYLD_FALLBACK_LIBRARY_PATH'] = OLD_FALLBACK_LIB
        os.environ['DYLD_FALLBACK_LIBRARY_PATH'] = ':'.join([libdir, OLD_FALLBACK_LIB])

    try:
        OLD_FRAMEWORK_LIB = os.environ['DYLD_FRAMEWORK_PATH']
    except KeyError:
        os.environ['DYLD_FRAMEWORK_PATH'] = os.path.join(basedir, 'frameworks')
    else:
        os.environ['CHIMERA_DYLD_FRAMEWORK_PATH'] = OLD_FRAMEWORK_LIB
        os.environ['DYLD_FRAMEWORK_PATH'] = ':'.join([os.path.join(basedir, 'frameworks'),
                                                      OLD_FRAMEWORK_LIB])


__all__ = ('CHIMERA_BINARY',
           'CHIMERA_PREFIX',
           'CHIMERA_LOCATIONS',
           'NULL',
           '_patch_envvars',
           '_patch_paths',
           '_patch_libraries',
           'launch_ipython')
