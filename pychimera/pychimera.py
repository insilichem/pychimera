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
import runpy
import sys
import subprocess
import platform
import re
import tempfile
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

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
    # os.devnull is not supported in Windows... dirty workaround
    if sys.platform == 'win32':
        _, blank = tempfile.mkstemp(suffix='.py')
    else:
        blank = os.devnull
    chimeraInit.init(['', '--script', blank], debug=verbose,
                     silent=not verbose, nostatus=not verbose,
                     nogui=nogui, eventloop=not nogui, exitonquit=not nogui)
    if blank is not os.devnull:
        pass # remove tmpfile!
    del chimeraInit
    os.environ['CHIMERA_ENABLED'] = '1'

load_chimera = enable_chimera

#---------------------------------------------------------------
# Environment, paths, and more patchers
#---------------------------------------------------------------

# Prevent complains from standard interpreters when launched from Continuum builds
platform._sys_version_parser = re.compile(
    r'([\w.+]+)\s*(?:\|[^|]*\|)?\s*\(#?([^,]+),\s*([\w ]+),\s*([\w :]+)\)\s*\[([^\]]+)\]?')


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

    paths = guess_chimera_path(common_locations=nogui)
    CHIMERA = paths[0]
    if nogui:
        try:
            CHIMERA = next(p for p in paths if 'headless' in p)
        except StopIteration:
            pass
    
    os.environ['CHIMERA'] = CHIMERA
    CHIMERALIB = os.path.join(CHIMERA, 'lib')
    
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

    # Check interactive and IPython
    if in_ipython() and hasattr(sys, 'ps1') and not sys.argv[0].endswith('ipython'):
        sys.argv.insert(1, 'ipython')

    # Load Chimera libraries
    if sys.platform == 'win32':
        os.environ['PATH'] = ';'.join([os.path.join(CHIMERA, 'bin'),
                                       os.path.join(CHIMERA, 'bin', 'DLLs'),
                                       os.environ['PATH']])
        os.environ['PYTHONPATH'] = ';'.join(
            [os.path.join(CHIMERA, 'share'),
             os.path.join(CHIMERA, 'bin')] +
            (sys.path if nogui else []) +
            [os.path.join(CHIMERA, 'bin', 'lib', 'site-packages', 'suds_jurko-0.6-py2.7.egg'),
             os.path.join(CHIMERA, 'bin', 'python27.zip'),
             os.path.join(CHIMERA, 'bin', 'DLLs'),
             os.path.join(CHIMERA, 'bin', 'lib'),
             os.path.join(CHIMERA, 'bin', 'lib'),
             os.path.join(CHIMERA, 'bin', 'lib', 'plat-win'),
             os.path.join(CHIMERA, 'bin', 'lib', 'lib-tk'),
             os.path.join(CHIMERA, 'bin', 'lib', 'site-packages'),
             os.path.join(CHIMERA, 'bin', 'lib', 'site-packages', 'PIL'),
             os.path.join('C:', 'ProgramData', 'Chimera')])
    else:
        os.environ['PYTHONPATH'] = ':'.join(
            [os.path.join(CHIMERA, 'share'),
             os.path.join(CHIMERA, 'bin')]  +
            (sys.path if nogui else []) +
            [CHIMERALIB,
             os.path.join(CHIMERALIB, 'python2.7', 'site-packages', 'suds_jurko-0.6-py2.7.egg'),
             os.path.join(CHIMERALIB, 'python27.zip'),
             os.path.join(CHIMERALIB, 'python2.7'),
             os.path.join(CHIMERALIB, 'python2.7', 'plat-linux2'),
             os.path.join(CHIMERALIB, 'python2.7', 'lib-tk'),
             os.path.join(CHIMERALIB, 'python2.7', 'lib-old'),
             os.path.join(CHIMERALIB, 'python2.7', 'lib-dynload'),
             os.path.join(CHIMERALIB, 'python2.7', 'site-packages')])
        if sys.platform == 'darwin':
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
            sys.executable = os.path.join(CHIMERA, 'bin', 'python2.7')
            os.environ['FONTCONFIG_FILE'] = '/usr/X11/lib/X11/fonts/fonts.conf'
        else:
            try:
                OLDLIB = os.environ['LD_LIBRARY_PATH']
            except KeyError:
                os.environ['LD_LIBRARY_PATH'] = CHIMERALIB
            else:
                os.environ['CHIMERA_LD_LIBRARY_PATH'] = OLDLIB
                os.environ['LD_LIBRARY_PATH'] = ':'.join([CHIMERALIB, OLDLIB])

        os.environ['TERM'] = "xterm-256color"
        os.environ['PYTHONWARNINGS'] = "ignore"
    os.execve(sys.executable, [sys.executable] + sys.argv, os.environ)

def guess_chimera_path(common_locations=False):
    """
    Try to guess Chimera installation path.

    Parameters
    ----------
    common_locations : bool, optional, default=False
        If no CHIMERADIR env var is set, collect all posible
        locations of Chimera installations.

    Returns
    -------
    paths: list of str
        Alphabetically sorted list of possible Chimera locations
    """
    # First, check if environment variable is already present
    if 'CHIMERADIR' in os.environ:
        return os.environ['CHIMERADIR'],

    exit_message = ('ERROR: Platform not supported.\nPlease, create an environment '
                    'variable CHIMERADIR set to your Chimera installation path, or '
                    'softlink the chimera binary to somewhere in your $PATH.')
    if sys.platform.startswith('win') or sys.platform == 'cygwin':
        binary, prefix = 'chimera.exe', 'Chimera*'
        directories = map(os.getenv, ('PROGRAMFILES', 'PROGRAMFILES(X86)', 'PROGRAMW6432'))
    elif sys.platform.startswith('linux'):
        binary, prefix = 'chimera', 'UCSF-Chimera*'
        directories = [os.path.expanduser('~/.local')]
    elif sys.platform.startswith('darwin'):
        binary, prefix = 'chimera', 'Chimera*/Contents/Resources'
        directories = ['/Applications', os.path.expanduser('~/.local'),
                       os.path.expanduser('~/Desktop')]
    else:
        sys.exit(exit_message)

    try:
        return search_chimera(binary, directories, prefix, common_locations=common_locations)
    except IOError:  # 404 - Chimera not found!
        sys.exit(exit_message)


def search_chimera(binary, directories, prefix, common_locations=False):
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
    common_locations : bool, optional, default=False
        Collect all posible locations of Chimera installations, even if a 
        binary has been found.

    Returns
    -------
    paths : list of str
        Sorted list of Chimera paths. If found, the first one is the one returned
        by the binary call. Next items are the ones found in `directories`, sorted
        by descendent order.
    """
    paths = []
    try:
        paths.append(subprocess.check_output([binary, '--root']).decode('utf-8').strip())
    except (OSError, subprocess.CalledProcessError, RuntimeError, ValueError):
        common_locations = True
    if common_locations:
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

#---------------------------------------------------------------
# IPython, Jupyter and Notebook stuff
#---------------------------------------------------------------


def check_ipython(command, args):
    """
    Check if an IPython launch has been requested from CLI
    """
    if command == 'ipython':
        if sys.platform == 'win32':
            launch_ipython_windows(args)
        else:
            launch_ipython(args)

    elif command == 'notebook':
        launch_notebook(args)


def launch_ipython(argv=None):
    """
    Launch IPython from this interpreter with custom args if needed.
    Chimera magic commands are also enabled automatically.
    """
    try:
        from IPython.terminal.ipapp import TerminalIPythonApp
        from traitlets.config import Config
    except ImportError:
        sys.exit("ERROR: IPython not installed in this environment. "
                 "Try with `conda install ipython`")
    else:
        # launch_new_instance(argv)
        app = TerminalIPythonApp()
        c = Config()
        code = ["from pychimera import enable_chimera_inline",
                "enable_chimera_inline()"]
        c.InteractiveShellApp.exec_lines = code
        app.update_config(c)
        app.initialize(argv)
        app.start()


def launch_ipython_windows(argv=None):
    os.environ = {str(k): str(v) for k,v in os.environ.items()}
    try:
        from qtconsole.qtconsoleapp import JupyterQtConsoleApp
        from traitlets.config import Config
    except ImportError:
        sys.exit("ERROR: IPython QTConsole not installed in this environment. "
                 "Try with `conda install jupyter qtconsole`")
    else:
        app = JupyterQtConsoleApp()
        c = Config()
        code = ["from pychimera import enable_chimera_inline",
                "enable_chimera_inline()"]
        c.InteractiveShellApp.exec_lines = code
        app.update_config(c)
        app.initialize(argv)
        app.start()


def launch_notebook(argv=None):
    """
    Launch a Jupyter Notebook, with custom Untitled filenames and
    a prepopulated first cell with necessary boilerplate code.

    Notes
    -----
    To populate the first cell, the function `new_notebook` imported
    in notebook.services.contents needs to be monkey patched. Dirty
    but functional. Same thing could be achieved with custom.js or
    a ContentsManager subclass, but this is easier!
    """
    try:
        import nbformat.v4 as nbf
        from notebook.notebookapp import NotebookApp
        from notebook.services.contents import manager
        from traitlets.config import Config
    except ImportError:
        sys.exit("ERROR: Jupyter Notebook not installed in this environment. "
                 "Try with `conda install ipython jupyter notebook`")
    else:
        nbf._original_new_notebook = nbf.new_notebook
        def _prepopulate_nb_patch():
            nb = nbf._original_new_notebook()
            cell = nbf.new_code_cell("# Run this cell to complete Chimera initialization\n"
                                     "from pychimera import enable_chimera, enable_chimera_inline, chimera_view\n"
                                     "enable_chimera()\nenable_chimera_inline()\nimport chimera")
            nb['cells'].append(cell)
            return nb
        manager.new_notebook = _prepopulate_nb_patch
        app = NotebookApp()
        c = Config()
        c.FileContentsManager.untitled_notebook = "Untitled PyChimera Notebook"
        app.update_config(c)
        app.initialize(argv)
        app.start()


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


def enable_chimera_inline():
    """
    Enable IPython magic commands to run some Chimera actions

    Currently supported:
    - %chimera_export_3D [<model>]: 
        Depicts the Chimera 3D canvas in a WebGL iframe. Requires
        a headless Chimera build and a Notebook instance. SLOW.
    - %chimera_run <command>:
        Runs Chimera commands meant to be input in the GUI command line
    """

    from IPython.display import IFrame
    from IPython.core.magic import register_line_magic
    import chimera
    import Midas

    @register_line_magic
    def chimera_export_3D(line):
        if chimera.viewer.__class__.__name__ == 'NoGuiViewer':
            print('This magic requires a headless Chimera build. '
                  'Check http://www.cgl.ucsf.edu/chimera/download.html#unsupported.',
                  file=sys.stderr)
            return
        models = eval(line) if line else []

        def html(*models):
            if models:
                for m in chimera.openModels.list():
                    m.display = False
                chimera.selection.clearCurrent()
                for model in models:
                    model.display = True
                    chimera.selection.addCurrent(model)
                    chimera.runCommand('focus sel')
            chimera.viewer.windowSize = 800, 600
            path = 'chimera_scene_export.html'
            Midas.export(filename=path, format='WebGL')
            return IFrame(path, *[x + 20 for x in chimera.viewer.windowSize])
        return html(*models)
    del chimera_export_3D

    @register_line_magic
    def chimera_run(line):
        if not line:
            print("Usage: %chimera_run <chimera command>", file=sys.stderr)
            return
        chimera.runCommand(line)
    del chimera_run

def chimera_view(*molecules):
    """
    Depicts the requested molecules with NGLViewer in a Python notebook.
    This method does not require a headless Chimera build, however.

    Parameters
    ----------
    molecules : tuple of chimera.Molecule
        Molecules to display. If none is given, all present molecules
        in Chimera canvas will be displayed.
    """
    try:
        import nglview as nv
    except ImportError:
        raise ImportError('You must install nglview!')
    import chimera

    class _ChimeraStructure(nv.Structure):
        def __init__(self, *molecules):
            if not molecules:
                raise ValueError('Please supply at least one chimera.Molecule.')
            self.ext = "pdb"
            self.params = {}
            self.id = str(id(molecules[0]))
            self.molecules = molecules
    
        def get_structure_string(self):
            s = StringIO()
            chimera.pdbWrite(self.molecules, self.molecules[0].openState.xform, s)
            return s.getvalue()

    if not molecules:
        molecules = chimera.openModels.list(modelTypes=[chimera.Molecule])
    
    structure = _ChimeraStructure(*molecules)
    return nv.NGLWidget(structure)

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
    patch_environ(nogui=args.nogui)
    if args.command != 'notebook':
        enable_chimera(verbose=args.verbose, nogui=args.nogui)
    if args.nogui:
        check_ipython(args.command, more_args)
        run_cli_options(args)

if "__main__" == __name__:
    sys.exit(main())
