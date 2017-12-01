Usage
=====

Run ``pychimera -h`` for quick help.

To start an **interactive** Python session:

::

    pychimera                  # standalone
    pychimera -i some_file.py  # with some file
    pychimera -im module       # with a Python module
    pychimera -ic "string"     # with a command
    pychimera ipython          # launch IPython interpreter
    pychimera notebook         # launch IPython notebook
    pychimera --path           # print detected UCSF Chimera installation


To execute a script:

::

    pychimera script.py

To launch Chimera GUI with custom packages (check `InsiliChem Plume`_ as an example!):

::

    pychimera --gui

To launch a module that uses Chimera internally:

::

    pychimera -m this

To execute any Python statement:

::

    pychimera -c 'import chimera'


.. _InsiliChem Plume: https://github.com/insilichem/plume