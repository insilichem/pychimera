#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


CHIMERA_BINARY = 'chimera'
CHIMERA_PREFIX = 'UCSF-Chimera*'
CHIMERA_LOCATIONS = ('/opt',
                     os.path.expanduser('~/.local'))
NULL = os.devnull

def _patch_envvars(basedir, libdir, nogui=True):
    os.environ['TERM'] = "xterm-256color"
    # os.environ['PYTHONWARNINGS'] = "ignore"


def _patch_paths(basedir, libdir, nogui=True):
    os.environ['PYTHONPATH'] = ':'.join(
	    [os.path.join(basedir, 'share'),
	     os.path.join(basedir, 'bin')]  +
	    (sys.path if nogui else []) +
	    [libdir,
	     os.path.join(libdir, 'python2.7', 'site-packages', 'suds_jurko-0.6-py2.7.egg'),
	     os.path.join(libdir, 'python27.zip'),
	     os.path.join(libdir, 'python2.7'),
	     os.path.join(libdir, 'python2.7', 'plat-linux2'),
	     os.path.join(libdir, 'python2.7', 'lib-tk'),
	     os.path.join(libdir, 'python2.7', 'lib-old'),
	     os.path.join(libdir, 'python2.7', 'lib-dynload'),
	     os.path.join(libdir, 'python2.7', 'site-packages')])


def _patch_libraries(basedir, libdir, nogui=True):
    try:
        OLDLIB = os.environ['LD_LIBRARY_PATH']
    except KeyError:
        os.environ['LD_LIBRARY_PATH'] = libdir
    else:
        os.environ['CHIMERA_LD_LIBRARY_PATH'] = OLDLIB
        os.environ['LD_LIBRARY_PATH'] = ':'.join([libdir, OLDLIB])


def launch_ipython(argv=None, ipython_app=None):
    """
    Launch IPython from this interpreter with custom args if needed.
    Chimera magic commands are also enabled automatically.
    """
    try:
        if ipython_app is None:
            from IPython.terminal.ipapp import TerminalIPythonApp as ipython_app
        from traitlets.config import Config
    except ImportError:
        sys.exit("ERROR: IPython not installed in this environment. "
                 "Try with `conda install ipython`")
    else:
        # launch_new_instance(argv)
        app = ipython_app()
        c = Config()
        code = ["from pychimera import enable_chimera_inline",
                "enable_chimera_inline()"]
        c.InteractiveShellApp.exec_lines = code
        app.update_config(c)
        app.initialize(argv)
        app.start()

__all__ = ('CHIMERA_BINARY',
           'CHIMERA_PREFIX',
           'CHIMERA_LOCATIONS',
           'NULL',
           '_patch_envvars',
           '_patch_paths',
           '_patch_libraries',
           'launch_ipython')