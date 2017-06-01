#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from tempfile import mkstemp as _mkstemp
from distutils.spawn import find_executable as _find_executable

CHIMERA_BINARY = 'chimera.exe'
CHIMERA_PREFIX = 'Chimera*'
CHIMERA_LOCATIONS = map(os.getenv, ('PROGRAMFILES', 'PROGRAMFILES(X86)', 'PROGRAMW6432'))
_fh, NULL = _mkstemp(suffix='.py')


def _patch_envvars(*args, **kwargs):
    pass


def _patch_libraries(*args, **kwargs):
    pass


def _patch_paths(basedir, libdir, nogui=True):
    os.environ['PATH'] = ';'.join([os.path.join(basedir, 'bin'),
                                   os.path.join(basedir, 'bin', 'DLLs'),
                                   os.path.join(basedir, 'bin', 'lib'),
                                   os.environ['PATH']])
    os.environ['PYTHONPATH'] = ';'.join(
        [os.path.join(basedir, 'share'),
         os.path.join(basedir, 'bin')]
        + (sys.path if nogui else []) +
        [os.path.join(basedir, 'bin', 'lib', 'site-packages', 'setuptools-3.1-py2.7.egg'),
         os.path.join(basedir, 'bin', 'lib', 'site-packages', 'suds_jurko-0.6-py2.7.egg'),
         os.path.join(basedir, 'bin', 'DLLs'),
         os.path.join(basedir, 'bin', 'libs'),
         os.path.join(basedir, 'bin', 'lib'),
         os.path.join(basedir, 'bin', 'lib', 'lib-tk'),
         os.path.join(basedir, 'bin', 'lib', 'plat-win'),
         os.path.join(basedir, 'bin', 'lib', 'site-packages'),
         os.path.join(basedir, 'bin', 'lib', 'site-packages', 'PIL'),
         basedir])


def launch_ipython(argv=None):
    """
    Force usage of QtConsole under Windows
    """
    from .linux import launch_ipython as _launch_ipython_linux
    os.environ = {str(k): str(v) for k,v in os.environ.items()}
    try:
        from qtconsole.qtconsoleapp import JupyterQtConsoleApp
    except ImportError:
        sys.exit("ERROR: IPython QtConsole not installed in this environment. "
                 "Try with `conda install jupyter ipython qtconsole`")
    else:
        _launch_ipython_linux(ipython_app=JupyterQtConsoleApp)


__all__ = ('CHIMERA_BINARY',
           'CHIMERA_PREFIX',
           'CHIMERA_LOCATIONS',
           'NULL',
           '_patch_envvars',
           '_patch_paths',
           '_patch_libraries',
           'launch_ipython')