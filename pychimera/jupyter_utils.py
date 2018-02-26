#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python, Jupyter and Notebook stuff
"""

from __future__ import print_function
import sys
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from .platforms import launch_ipython


def check_ipython(command, args):
    """
    Check if an IPython launch has been requested from CLI
    """
    if command == 'ipython':
        launch_ipython(args)
    elif command == 'notebook':
        launch_notebook(args)


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


#---------------------------------------------------------------
# Magics!
#---------------------------------------------------------------

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