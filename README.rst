PyChimera
=========

.. image:: https://travis-ci.org/insilichem/pychimera.svg?branch=master
   :target: https://travis-ci.org/insilichem/pychimera

.. image:: https://zenodo.org/badge/50309940.svg
   :target: https://zenodo.org/badge/latestdoi/50309940


Use `UCSF Chimera`_ packages in any Python 2.7 interpreter

With PyChimera you can…

-  Run scripts depending on chimera **from CLI** with ``pychimera``.
-  Enable ``import chimera`` in interactive coding sessions (console, ipython)
   **outside Chimera**.
-  Use Jupyter Notebooks with Chimera. You only need to run the prepopulated cell.
-  Launch a standard Chimera instance, with the benefit of importing all
   your conda or virtualenv packages with ``pychimera --gui``.

I hope it’s useful! Feedback is appreciated!

*While we intend to offer multiplatform support, it has been only tested on
Linux. Some rough edges could arise in Windows & Mac. Please submit an issue
if you find any problems!*

Installation
------------

First, if you haven’t already, install `latest UCSF Chimera`_. We recommend
using it inside a Python 2.7 `conda <https://conda.io/miniconda.html>`_ environment.

Then, install PyChimera via ``pip`` or ``setup.py``:

::

    pip install pychimera

    git clone https://github.com/insilichem/pychimera.git && python pychimera/setup.py install



Usage
-----

Run ``pychimera -h`` for quick help.

To start an interactive Python session:

::

    pychimera                  # standalone
    pychimera -i some_file.py  # with some file
    pychimera -im module       # with a Python module
    pychimera -ic "string"     # with a command
    pychimera ipython          # launch IPython interpreter
    pychimera notebook         # launch IPython notebook

To launch a module that uses Chimera internally:

::

    pychimera -m this

To execute any Python statement:

::

    pychimera -c 'import chimera'

To execute a script:

::

    pychimera script.py

To launch Chimera GUI with custom packages:

::

    pychimera --gui



For developers
--------------

PyChimera provides access to Chimera’s modules from any Python 2.x
interpreter. This is achieved in two steps:

1. ``patch_environ()`` patches environment variables with proper paths
   (packages and libraries). Since the original ``sys.path`` is exported
   to ``PYTHONPATH``, you can use all your virtualenv/conda packages
   with Chimera. This call restarts Python to inject a new
   ``os.environ`` with ``os.execve``.

2. ``enable_chimera()`` initializes Chimera. This is done through their
   own routines (``chimeraInit``).

PyChimera also offers its interface through python ``-m``. This has not
been tested, so it may not work. Add ``-i`` for interactive mode:

::

    python -[i]m pychimera [-m another_module | -c "string" | script.py | ipython | notebook]

You can also try to launch it from IPython, but, again, some things may not
work. Anyway, these two commands have the same effect:

::

    pychimera ipython [notebook]
    ipython -m pychimera [notebook]

If you want to run a script with IPython and then inspect the results
(``-i`` flag), your best bet is to run ``pychimera ipython`` and then
call ``%run path/to/file.py`` inside the interpreter.

Notes
-----

Obviously, you need to install `latest UCSF Chimera`_ in your computer. PyChimera
will do its best to find the installation path automagically in the standard
locations. If somehow it doesn’t succeed, you can always set an environment variable
called ``CHIMERADIR`` in your ``.bashrc``, or similar.

::

    export CHIMERADIR="~/.local/UCSF-Chimera"


Known issues
------------

Chimera bundles its own distribution of some popular packages, like
numpy, and those are loaded before your env packages for compatibility
reasons. Be warned if you use specific versions for your project,
because you can face strange bugs if you don’t take this into account.

In some platforms (Linux), this can be worked around with some work on
the precendence of paths in ``sys.path``, but in some of them not (OS X).
The easiest and most robust way to fix this is by upgrading Chimera's ``numpy``:

::

    pip install --upgrade numpy -t `pychimera --path`/lib/python2.7/site-packages

If you use the development version of pychimera, Chimera's setuptools will complain
about the versioning scheme (ie, ``pychimera==0.1.11+6.gc2e1fbb.dirty``). As before,
the fix is to upgrade the package. You might have to remove it beforehand, though:

::

    rm -r `pychimera --path`/lib/python2.7/site-packages/setuptools-3.1*
    pip install --upgrade setuptools -t `pychimera --path`/lib/python2.7/site-packages



Acknowledgments
---------------

Largely based on ideas by `Greg Couch at chimera-users`_.

.. _UCSF Chimera: https://www.cgl.ucsf.edu/chimera/
.. _latest UCSF Chimera: http://www.cgl.ucsf.edu/chimera/download.html
.. _Greg Couch at chimera-users: http://www.cgl.ucsf.edu/pipermail/chimera-users/2015-January/010647.html


Citation
--------

.. image:: https://zenodo.org/badge/50309940.svg
   :target: https://zenodo.org/badge/latestdoi/50309940

PyChimera is scientific software, funded by public research grants
(Spanish MINECO's project ``CTQ2014-54071-P``, Generalitat de Catalunya's
project ``2014SGR989`` and research grant ``2015FI_B00768``, COST Action ``CM1306``).
If you make use of PyChimera in scientific publications, please cite it. It will help
measure the impact of our research and future funding!

.. code-block:: latex

    @misc{jaime_rgp_2017_546883,
      author       = {Jaime Rodríguez-Guerra Pedregal and
                      Jean-Didier Maréchal},
      title        = {insilichem/pychimera: PyChimera},
      month        = apr,
      year         = 2017,
      doi          = {10.5281/zenodo.546883},
      url          = {https://doi.org/10.5281/zenodo.546883}
    }