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
__version_info__ = (0, 1, 6)
__version__ = '.'.join(map(str, __version_info__))


def patch_environ(nogui=True):
    """
    Patch current environment variables so Chimera can start up and we can import its modules.

    Be warned that calling this function WILL restart your interpreter. Otherwise, Python
    won't catch the new LD_LIBRARY_PATH (or platform equivalent) and Chimera won't find its
    libraries during import.
    """
    patch_sys_version()
    if 'CHIMERA' in os.environ:
        return
   
    os.environ['CHIMERA'] = CHIMERA = guess_chimera_path()[-1]
    CHIMERALIB = os.path.join(CHIMERA, 'lib')
    os.environ['PYTHONPATH'] = ":".join([
        CHIMERALIB,
        os.path.join(CHIMERA, 'share'),
        os.path.join(CHIMERA, 'bin'),
        os.path.join(CHIMERALIB, 'python2.7', 'site-packages', 'suds_jurko-0.6-py2.7.egg'),
        os.path.join(CHIMERALIB, 'python27.zip'),
        os.path.join(CHIMERALIB, 'python2.7'),
        os.path.join(CHIMERALIB, 'python2.7', 'plat-linux2'),
        os.path.join(CHIMERALIB, 'python2.7', 'lib-tk'),
        os.path.join(CHIMERALIB, 'python2.7', 'lib-old'),
        os.path.join(CHIMERALIB, 'python2.7', 'lib-dynload'),
        os.path.join(CHIMERALIB, 'python2.7', 'site-packages')] + sys.path)

    # Set Tcl/Tk for gui mode
    if 'TCL_LIBRARY' in os.environ:
        os.environ['CHIMERA_TCL_LIBRARY'] = os.environ['TCL_LIBRARY']
    os.environ['TCL_LIBRARY'] = os.path.join(CHIMERALIB, 'tcl8.6')
    if 'TCLLIBPATH' in os.environ:
        os.environ['CHIMERA_TCLLIBPATH'] = os.environ['TCLLIBPATH']
    os.environ['TCLLIBPATH'] = '{' + CHIMERALIB + '}'
    if 'TK_LIBRARY' in os.environ:
        os.environ['CHIMERA_TK_LIBRARY'] = os.environ['TK_LIBRARY']
        del os.environ['TK_LIBRARY']
    if 'TIX_LIBRARY' in os.environ:
        os.environ['CHIMERA_TIX_LIBRARY'] = os.environ['TIX_LIBRARY']
        del os.environ['TIX_LIBRARY']
    if 'PYTHONNOUSERSITE' in os.environ:
        os.environ['CHIMERA_PYTHONNOUSERSITE'] = os.environ['PYTHONNOUSERSITE']
    os.environ['PYTHONNOUSERSITE'] = '1'

    # Load Chimera libraries
    if sys.platform == 'win32':
        os.environ['PATH'] += ":" + CHIMERALIB
    elif sys.platform == 'darwin':
        try:
            OLD_FALLBACK_LIB = os.environ['DYLD_FALLBACK_LIBRARY_PATH']
        except KeyError:
            os.environ['DYLD_FALLBACK_LIBRARY_PATH'] = CHIMERALIB
        else:
            os.environ['CHIMERA_DYLD_FALLBACK_LIBRARY_PATH'] = OLD_FALLBACK_LIB
            os.environ['DYLD_FALLBACK_LIBRARY_PATH'] = ':'.join([CHIMERALIB, OLD_FALLBACK_LIB])

        try:
            OLD_FRAMEWORK_LIB = os.environ['DYLD_FRAMEWORK_PATH']
        except KeyError:
            os.environ['DYLD_FRAMEWORK_PATH'] = os.path.join(CHIMERA, 'frameworks')
        else:
            os.environ['CHIMERA_DYLD_FRAMEWORK_PATH'] = OLD_FRAMEWORK_LIB
            os.environ['DYLD_FRAMEWORK_PATH'] = ':'.join([os.path.join(CHIMERA, 'frameworks'),
                                                          OLD_FRAMEWORK_LIB])

        os.environ['FONTCONFIG_FILE'] = '/usr/X11/lib/X11/fonts/fonts.conf'
        sys.executable = os.path.join(CHIMERA, 'bin', 'python2.7')
    else:
        try:
            OLDLIB = os.environ['LD_LIBRARY_PATH']
        except KeyError:
            os.environ['LD_LIBRARY_PATH'] = CHIMERALIB
        else:
            os.environ['CHIMERA_LD_LIBRARY_PATH'] = OLDLIB
            os.environ['LD_LIBRARY_PATH'] = ':'.join([CHIMERALIB, OLDLIB])

    os.environ['TERM'] = "xterm-256color"

    # Check interactive and IPython
    if in_ipython() and hasattr(sys, 'ps1') and not sys.argv[0].endswith('ipython'):
        sys.argv.insert(1, 'ipython')

    os.execve(sys.executable, [sys.executable] + sys.argv, os.environ)


def enable_chimera(verbose=False, nogui=True):
    """
    Bypass script loading and initialize Chimera correctly.

    Parameters
    ----------
    verbose : bool, optional, default=False
        If True, let Chimera speak freely. It can be _very_ verbose.
    nogui : bool, optional, default=True
        Don't start the GUI.
    """
    try:
        import chimeraInit
    except ImportError as e:
        sys.exit(str(e) + "\nERROR: Chimera could not be loaded!")
    chimeraInit.init(['', '--script', os.devnull], debug=verbose,
                     silent=not verbose, nostatus=not verbose,
                     nogui=nogui, eventloop=not nogui, exitonquit=not nogui)
    del chimeraInit

load_chimera = enable_chimera


def guess_chimera_path():
    """
    Try to guess Chimera installation path.

    Returns
    -------
    paths: list of str
        Alphabetically sorted list of possible Chimera locations
    """
    # First, check if environment variable is already present
    if 'CHIMERADIR' in os.environ:
        return os.environ['CHIMERADIR'],

    # No luck... try workarounds
    if sys.platform.startswith('win') or sys.platform == 'cygwin':
        binary, prefix = 'chimera.exe', 'Chimera*'
        directories = map(os.getenv, ('PROGRAMFILES', 'PROGRAMFILES(X86)', 'PROGRAMW6432'))
    elif sys.platform.startswith('linux'):
        binary, prefix = 'chimera', 'UCSF-Chimera*'
        directories = [os.path.expanduser('~/.local')]
    elif sys.platform.startswith('darwin'):
        binary, prefix = 'chimera', 'Chimera*/Contents/Resources'
        directories = ['/Applications', os.path.expanduser('~/.local'), os.path.expanduser('~/Desktop')]
    else:
        sys.exit('ERROR: Platform not supported.\nPlease, create an environment '
                 'variable CHIMERADIR set to your Chimera installation path, or '
                 'softlink the chimera binary to somewhere in your $PATH.')

    try:
        return search_chimera(binary, directories, prefix)
    except IOError:  # 404 - Chimera not found!
        sys.exit('ERROR: Platform not supported.\nPlease, create an environment '
                 'variable CHIMERADIR set to your Chimera installation path, or '
                 'softlink the chimera binary to somewhere in your $PATH.')


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
        return subprocess.check_output([binary, '--root']).decode('utf-8').strip(),
    except (OSError, subprocess.CalledProcessError, RuntimeError, ValueError):
        for basedir in directories:
            paths = filter(os.path.isdir, glob(os.path.join(basedir, prefix)))
            if paths:
                paths.sort()
                return paths
    raise IOError  # 404 - Chimera not found


def patch_sys_version():
    """ Remove Continuum copyright statement to avoid parsing errors in IDLE """
    if '|' in sys.version:
        sys_version = sys.version.split('|')
        sys.version = ' '.join([sys_version[0].strip(), sys_version[-1].strip()])


def parse_cli_options(argv=None):
    parser = ArgumentParser(description='pychimera - UCSF Chimera for standard Python')
    parser.add_argument('-i', action='store_true', dest='interactive', default=False,
                        help='Enable interactive mode')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False,
                        help='Print debug information')
    parser.add_argument('--gui', action='store_false', dest='nogui', default=True,
                        help='Launch Chimera graphical interface')

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
    if interactive_mode(args.interactive):
        os.environ['PYTHONINSPECT'] = 'yes'


def check_ipython(command, args):
    """
    Check if an IPython launch has been requested from CLI
    """
    if command == 'ipython':
        launch_ipython(args)
    elif command == 'notebook':
        print('-'*56)
        print('Remember to call pychimera.enable_chimera() from a cell!')
        print('-'*56)
        launch_ipython(['notebook'] + args)


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


def interactive_mode(interactive_flag=False):
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
    args, more_args = parse_cli_options()
    patch_environ(nogui=args.nogui)
    if args.command != 'notebook':
        enable_chimera(verbose=args.verbose, nogui=args.nogui)
    if args.nogui:
        check_ipython(args.command, more_args)
        run_cli_options(args)

if "__main__" == __name__:
    main()
