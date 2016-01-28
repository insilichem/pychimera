#!/usr/bin/env python2
# -*- coding: utf-8 -*-


"""
pychimera
=========

Use UCSF Chimera Python API in a standard Python 2.7 interpreter.
"""

from __future__ import division, print_function
from argparse import ArgumentParser
from glob import glob
import os
import runpy
import sys
import subprocess

__author__ = "Jaime Rodríguez-Guerra"
__version_info__ = (0, 1, 0)
__version__ = '.'.join(map(str, __version_info__))


def patch_environ():
    """
    Patch current environment variables so Chimera can start up and we can import its modules.

    Be warned that calling this function WILL restart your interpreter. Otherwise, Python
    won't catch the new LD_LIBRARY_PATH (or platform equivalent) and Chimera won't find its
    libraries during import.
    """
    if 'CHIMERA' not in os.environ:
        os.environ['TERM'] = "xterm-256color"
        CHIMERA = os.environ['CHIMERA'] = os.environ['PYTHONHOME'] = guess_chimera_path()

        # PYTHONPATH defines additional locations where Python should look for packages
        os.environ['PYTHONPATH'] = ":".join([os.path.join(CHIMERA, 'bin'),
                                             os.path.join(CHIMERA, 'share'),
                                             os.path.join(CHIMERA, 'lib')]
                                            + sys.path)  # don't forget current packages!

        # Load Chimera libraries
        CHIMERALIB = os.path.join(CHIMERA, 'lib')
        if sys.platform == 'win32':
            os.environ['PATH'] += ":" + CHIMERALIB
        elif sys.platform == 'darwin':
            OLDLIB = os.environ.getenv('DYLD_LIBRARY_PATH', '')
            os.environ['DYLD_LIBRARY_PATH'] = ':'.join([CHIMERALIB, OLDLIB])
        else:
            OLDLIB = os.environ.get('LD_LIBRARY_PATH', '')
            os.environ['LD_LIBRARY_PATH'] = ':'.join([CHIMERALIB, OLDLIB])

        # Check interactive and IPython
        if in_ipython() and hasattr(sys, 'ps1') and not sys.argv[0].endswith('ipython'):
            sys.argv.insert(1, 'ipython')

        os.execve(sys.executable, [sys.executable] + sys.argv, os.environ)


def load_chimera(verbose=False):
    """
    Bypass script loading and initialize Chimera in nogui mode.

    Parameters
    ----------
    verbose : bool, optional, default=False
        If True, let Chimera speak freely. It can be _very_ verbose.
    """
    import chimeraInit
    if verbose:
        verbosity = ['--debug']
    else:
        verbosity = ['--nostatus', '--silent']
    chimeraInit.init([''] + verbosity + ['--script', os.devnull],
                     nogui=True, eventloop=False, exitonquit=False)
    del chimeraInit


def guess_chimera_path():
    """
    Try to guess Chimera installation path
    """
    # First, check if environment variable is already present
    if 'CHIMERADIR' in os.environ:
        return os.environ['CHIMERADIR']

    # No luck... try workarounds
    if sys.platform.startswith('win') or sys.platform == 'cygwin':
        binary, prefix = 'chimera.exe', 'Chimera'
        directories = map(os.getenv, ('PROGRAMFILES', 'PROGRAMFILES(X86)', 'PROGRAMW6432'))
    elif sys.platform.startswith('linux'):
        binary, prefix = 'chimera', 'UCSF-Chimera'
        directories = [os.path.expanduser('~/.local')]
    else:
        sys.exit('ERROR: Platform not supported.\nPlease, create an environment'
                 'variable CHIMERADIR set to your Chimera installation path.')

    try:
        return search_chimera(binary, directories, prefix)
    except IOError:  # 404 - Chimera not found!
        sys.exit('ERROR: Chimera installation path could not be found.\nPlease, '
                 'create an environment variable CHIMERADIR with such path.')


def search_chimera(binary, directories, prefix):
    """
    Try running ``chimera --root`` in Chimera happens to be in PATH, otherwise
    traverse usual installation locations to find the Chimera root path.

    Parameters
    ----------
    binary : str
        Name of the chimera executable in this platform
    directories: list of str
        Usual installation locations in this platform
    prefix : str
        Root directory prefix name in this platform

    Returns
    -------
    paths : list of str
        Sorted list of Chimera paths
    """
    try:
        return subprocess.check_output([binary, '--root']).decode('utf-8').strip()
    except (OSError, subprocess.CalledProcessError, RuntimeError):
        for basedir in directories:
            paths = filter(os.path.isdir, glob(os.path.join(basedir, prefix+'*')))
            if paths:
                paths.sort()
                return paths
    raise IOError  # 404 - Chimera not found


def parse_cli_options(argv=None):
    parser = ArgumentParser(description='pychimera - UCSF Chimera for standard Python')
    parser.add_argument('-i', action='store_true', dest='interactive',
                        help='Enable interactive mode')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('command', nargs='?',
                       help="A keyword {ipython, notebook} or a Python script")
    group.add_argument('-m', dest='module', help='Run Python module as a script')
    group.add_argument('-c', dest='string', help='Program passed in as string')

    global args, more_args
    args, more_args = parser.parse_known_args(argv)


def run_cli_options():
    """
    Quick implementation of Python interpreter's -m, -c and file execution.
    The resulting dictionary is imported into global namespace, just in case
    someone is using interactive mode.
    """
    global args, more_args
    if not in_ipython():
        if args.module:
            globals().update(runpy.run_module(args.module, run_name="__main__"))
        if args.string:
            exec(args.string)
        if args.command not in ('ipython', 'notebook', None):
            oldargv, sys.argv = sys.argv, sys.argv[1:]
            globals().update(runpy.run_path(args.command, run_name="__main__"))
            sys.argv = oldargv
    if interactive_mode():
        os.environ['PYTHONINSPECT'] = 'yes'


def check_ipython():
    """
    Check if an IPython launch has been requested from CLI
    """
    global args, more_args
    if args.command == 'ipython':
        launch_ipython(more_args)
    elif args.command == 'notebook':
        launch_ipython(['notebook'] + more_args)


def launch_ipython(argv=None):
    """
    Launch IPython from this interpreter with custom args if needed
    """
    try:
        from IPython.terminal.ipapp import launch_new_instance
    except ImportError:
        sys.exit("ERROR: IPython not installed in this environment.")
    else:
        try:
            launch_new_instance(argv)
        except ImportError as e:
            if 'notebook' in str(e):
                sys.exit("ERROR: IPython notebook not installed in this environment.")
            raise


def in_ipython():
    """
    Is this being executed inside an IPython session?
    """
    return hasattr(__builtins__, '__IPYTHON__')


def interactive_mode():
    """
    Check if we need to relaunch Python in interactive mode:
    """
    global args
    return any([args.interactive, sys.flags.interactive, len(sys.argv) <= 1])


def enable_chimera(warn=True):
    """
    A simple alias to be called from interactive sessions, like IPython notebooks.
    """
    patch_environ()
    load_chimera()


def main():
    """
    1. Patch the environment with Python and libraries paths. This relaunches Python!
    2. Parse argv to see if we need to launch IPython before Chimera.
    3. Launch IPython if requested
    4. Load Chimera. IPython can import it now!
    5. Run any additional CLI arguments (-m, -c, -f), if needed
    """
    parse_cli_options()
    patch_environ()
    check_ipython()
    load_chimera()
    run_cli_options()


if "__main__" == __name__:
    main()
