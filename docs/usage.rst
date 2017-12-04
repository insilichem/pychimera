Usage
=====

Run ``pychimera -h`` for quick help. Basically:

Running code
------------

To execute a script:

::

    pychimera script.py


To launch a module that uses UCSF Chimera internally:

::

    pychimera -m this


To execute any Python statement:

::

    pychimera -c 'import chimera'

To know which UCSF Chimera instance is being loaded:

::

    pychimera --path


Interactive sessions
--------------------

To start an **interactive** Python session with importable UCSF Chimera modules:

::

    pychimera                  # start the standard Python interpreter
    pychimera -i some_file.py  # run a script and stay in the standard Python interpreter
    pychimera -im module       # same, but with a Python module
    pychimera -ic "string"     # same, but with a command
    pychimera ipython          # launch IPython interpreter
    pychimera notebook         # launch IPython notebook


To launch the UCSF Chimera GUI with custom packages (check `InsiliChem Plume`_ as an example!):

::

    pychimera --gui

.. _InsiliChem Plume: https://github.com/insilichem/plume