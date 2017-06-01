#!/usr/bin/env python
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
import platform
import re
import runpy
import subprocess
import sys

from .platforms import *
from .jupyter_utils import check_ipython, in_ipython

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


#---------------------------------------------------------------
# Chimera initializer
#---------------------------------------------------------------


def enable_chimera(verbose=False, nogui=True):
    """
    Bypass script loading and initialize Chimera correctly, once
    the env has been properly patched.

    Parameters
    ----------
    verbose : bool, optional, default=False
        If True, let Chimera speak freely. It can be _very_ verbose.
    nogui : bool, optional, default=True
        Don't start the GUI.
    """
    if os.getenv('CHIMERA_ENABLED'):
        return
    try:
        import chimeraInit
    except ImportError as e:    
        sys.exit(str(e) + "\nERROR: Chimera could not be loaded!")
    import Tix
    if 'TIX_LIBRARY' in os.environ:
        del os.environ['TIX_LIBRARY']
    chimeraInit.init(['', '--script', NULL], debug=verbose,
                     silent=not verbose, nostatus=not verbose,
                     nogui=nogui, eventloop=not nogui, exitonquit=not nogui)
    del chimeraInit, Tix 
    os.environ['CHIMERA_ENABLED'] = '1'

load_chimera = enable_chimera


#---------------------------------------------------------------
# Environment, paths, and more patchers
#---------------------------------------------------------------

# Prevent complaints from standard interpreters when launched from Continuum builds
platform._sys_version_parser = re.compile(
    r'([\w.+]+)\s*'
    '(?:\|[^|]*\|)?\s*\(#?([^,]+),\s*([\w ]+),\s*'
    '([\w :]+)\)\s*\[([^\]]+)\]?')

def patch_sys_version():
    """ Remove Continuum copyright statement to avoid parsing errors in IDLE """
    if '|' in sys.version:
        sys_version = sys.version.split('|')
        sys.version = ' '.join([sys_version[0].strip(), sys_version[-1].strip()])


def patch_environ(nogui=True):
    """
    Patch current environment variables so Chimera can start up and we can import its modules.

    Be warned that calling this function WILL restart your interpreter. Otherwise, Python
    won't catch the new LD_LIBRARY_PATH (or platform equivalent) and Chimera won't find its
    libraries during import.

    Parameters
    ----------
    nogui : bool, optional, default=False
        If the GUI is not going to be launched, try to locate a headless
        Chimera build to enable inline Chimera visualization.
    """
    if 'CHIMERA' in os.environ:
        return

    paths = guess_chimera_path(search_all=nogui)
    CHIMERA_BASE = paths[0]
    if nogui:  # try finding a headless version
        try:
            CHIMERA_BASE = next(p for p in paths if 'headless' in p)
        except StopIteration:
            pass
    
    os.environ['CHIMERA'] = CHIMERA_BASE
    CHIMERA_LIB = os.path.join(CHIMERA_BASE, 'lib')
    
    # Set Tcl/Tk for gui mode
    if 'TCL_LIBRARY' in os.environ:
        os.environ['CHIMERA_TCL_LIBRARY'] = os.environ['TCL_LIBRARY']
    os.environ['TCL_LIBRARY'] = os.path.join(CHIMERA_LIB, 'tcl8.6')
    
    if 'TCLLIBPATH' in os.environ:
        os.environ['CHIMERA_TCLLIBPATH'] = os.environ['TCLLIBPATH']
    os.environ['TCLLIBPATH'] = '{' + CHIMERA_LIB + '}'
    
    if 'TK_LIBRARY' in os.environ:
        os.environ['CHIMERA_TK_LIBRARY'] = os.environ['TK_LIBRARY']
        del os.environ['TK_LIBRARY']
    
    if 'TIX_LIBRARY' in os.environ:
        os.environ['CHIMERA_TIX_LIBRARY'] = os.environ['TIX_LIBRARY']
        del os.environ['TIX_LIBRARY']

    if 'PYTHONNOUSERSITE' in os.environ:
        os.environ['CHIMERA_PYTHONNOUSERSITE'] = os.environ['PYTHONNOUSERSITE']
    os.environ['PYTHONNOUSERSITE'] = '1'

    # Check interactive and IPython
    if in_ipython() and hasattr(sys, 'ps1') and not sys.argv[0].endswith('ipython'):
        sys.argv.insert(1, 'ipython')

    # Platform-specific patches
    patch_environ_for_platform(CHIMERA_BASE, CHIMERA_LIB, nogui=nogui)
    os.execve(sys.executable, [sys.executable] + sys.argv, os.environ)


def guess_chimera_path(search_all=False):
    """
    Try to guess Chimera installation path.

    Parameters
    ----------
    search_all : bool, optional, default=False
        If no CHIMERADIR env var is set, collect all posible
        locations of Chimera installations.

    Returns
    -------
    paths: list of str
        Alphabetically sorted list of possible Chimera locations
    """    
    try:
        return _search_chimera(CHIMERA_BINARY, CHIMERA_LOCATIONS, CHIMERA_PREFIX,
                              search_all=search_all)
    except IOError:  # 404 - Chimera not found!
        sys.exit("Could not find UCSF Chimera.\n{}".format(_INSTRUCTIONS))


def _search_chimera(binary, directories, prefix, search_all=False):
    """
    Try running ``chimera --root`` if Chimera happens to be in PATH, otherwise
    traverse usual installation locations to find the Chimera root path.

    Parameters
    ----------
    binary : str
        Name of the chimera executable in this platform
    directories: list of str
        Usual installation locations in this platform
    prefix : str
        Root directory prefix name in this platform
    search_all : bool, optional, default=False
        Collect all posible locations of Chimera installations, even if a 
        binary has been found.

    Returns
    -------
    paths : list of str
        Sorted list of Chimera paths. If found, the first one is the one returned
        by the binary call. Next items are the ones found in `directories`, sorted
        by descendent order.
    """
    # First, check if environment variable is already present
    try:
        return os.environ['CHIMERADIR'],
    except KeyError:
        pass


    paths = []
    try:
        # Try with distutils.spawn.find_executable and save that subprocess!
        paths.append(subprocess.check_output([binary, '--root']).decode('utf-8').strip())
    except (OSError, subprocess.CalledProcessError, RuntimeError, ValueError):
        search_all = True
    
    if search_all:
        for basedir in directories:
            found_paths = filter(os.path.isdir, glob(os.path.join(basedir, prefix)))
            if found_paths:
                found_paths.sort()
                found_paths.reverse()
                paths.extend(found_paths)
    return paths


#---------------------------------------------------------------
# CLI stuff
#---------------------------------------------------------------


def parse_cli_options(argv=None):
    parser = ArgumentParser(description='pychimera - UCSF Chimera for standard Python')
    parser.add_argument('-i', action='store_true', dest='interactive', default=False,
                        help='Enable interactive mode')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False,
                        help='Print debug information')
    parser.add_argument('-V', '--version', action='version', 
                        version='%(prog)s v{}'.format(__version__))
    parser.add_argument('--gui', action='store_false', dest='nogui', default=True,
                        help='Launch Chimera graphical interface')
    parser.add_argument('--path', action='store_true', dest='path', default=False,
                        help='Return first found Chimera path')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('command', nargs='?',
                       help="A keyword {ipython, notebook} or a Python script")
    group.add_argument('-m', dest='module', help='Run Python module as a script')
    group.add_argument('-c', dest='string', help='Program passed in as string')

    return parser.parse_known_args(argv)


def run_cli_options(args):
    """
    Quick implementation of Python interpreter's -m, -c and file execution.
    The resulting dictionary is imported into global namespace, just in case
    someone is using interactive mode.
    """
    if not in_ipython():
        if args.module:
            globals().update(runpy.run_module(args.module, run_name="__main__"))
        if args.string:
            exec(args.string)
        if args.command not in ('ipython', 'notebook', None):
            oldargv, sys.argv = sys.argv, sys.argv[1:]
            globals().update(runpy.run_path(args.command, run_name="__main__"))
            sys.argv = oldargv
    if _interactive_mode(args.interactive):
        os.environ['PYTHONINSPECT'] = '1'


def _interactive_mode(interactive_flag=False):
    """
    Check if we need to relaunch Python in interactive mode:
    """
    return any([interactive_flag, sys.flags.interactive, len(sys.argv) <= 1])


def main():
    """
    1. Parse CLI arguments.
    2. Patch the environment with Python and libraries paths. This relaunches Python!
    3. Launch IPython if requested
    4. Load Chimera. IPython can import it now!
    5. Run any additional CLI arguments (-m, -c, -f), if needed
    """
    patch_sys_version()
    args, more_args = parse_cli_options()
    if args.path:
        print(guess_chimera_path()[0])
        return
    patch_environ(nogui=args.nogui)
    if args.command != 'notebook':
        enable_chimera(verbose=args.verbose, nogui=args.nogui)
    if args.nogui:
        check_ipython(args.command, more_args)
        run_cli_options(args)


if "__main__" == __name__:
    sys.exit(main())
