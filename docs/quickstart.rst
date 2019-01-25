Quickstart
==========

PyChimera lets you use the full UCSF Chimera codebase in any Python 2.7 project.

Why?
----

UCSF Chimera is an extensible molecular visualization tool with a vast collection
of modules gathered after years of development. These tools allow you to perform
serious molecular modelling jobs even without Python knowledge (they also offer
a very versatile text interface with `custom commands
<https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/framecommand.html>`_).

However, all this code is only available if you use the bundled Python 2.7 interpreter
to run your scripts, like this:

::

    chimera --nogui --script "path/to/my/script.py arg1 arg2 ..."


Or, using the GUI command line toolbar, by running ``runscript path/to/my/script.py
arg1 arg2 ...``. This is less desirable than simply running ``python script.py arg1 arg2 ...``.

With PyChimera, you can run ``pychimera script.py`` and forget about using the UCSF Chimera
interpreter or not. It just works. Additionally, it offers some more features:

- Interactive sessions in the Python interpreter where you can just run ``import chimera``,
  like it should be.

- Full compatibility with IPython and Jupyter Notebooks (read :ref:`ExtraPackages`).

- Simple API to run your Chimera-dependent script with any ``python`` interpreter.

- Conda recipes for UCSF Chimera and UCSF Chimera headless, for automated testing and deployment.

If you want more details, be sure to check the paper (already submitted, once published, it
will be linked here).

Usage
-----

Run ``pychimera -h`` for quick help. Basically:

Running code
............

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
....................

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


.. _multiplatform:

Multiplatform compatibility
---------------------------

.. image:: https://travis-ci.org/insilichem/pychimera.svg?branch=master
   :target: https://travis-ci.org/insilichem/pychimera

.. image:: https://ci.appveyor.com/api/projects/status/fwp3uum6be7tcfqn/branch/master?svg=true
   :target: https://ci.appveyor.com/project/jaimergp/pychimera


UCSF Chimera is available for Linux, Mac OS X and Windows. PyChimera does its best to
provide the same compatibility for all three platforms and each release is continuously
tested in `Travis CI`_ (Linux, Mac OS X) and `AppVeyor`_ (Windows). Despite our efforts,
some features might not be as polished in some platforms. The table below summarizes
the current state of implementation:

+-------------------------+-----------------------------+
|                         | Platforms                   |
+       Features          +-------+----------+----------+
|                         | Linux | Mac OS X | Windows* |
+=========================+=======+==========+==========+
| ``pychimera``           |   Y   |     Y    |    N     |
+-------------------------+-------+----------+----------+
| ``pychimera script.py`` |   Y   |     Y    |    Y     |
+-------------------------+-------+----------+----------+
| ``pychimera ipython``   |   Y   |     Y    |    Y**   |
+-------------------------+-------+----------+----------+
| ``pychimera notebook``  |   Y   |     Y    |    Y     |
+-------------------------+-------+----------+----------+
| ``pychimera --gui``     |   Y   |     Y    |    Y     |
+-------------------------+-------+----------+----------+
| ``pychimera -c``        |   Y   |     Y    |    Y     |
+-------------------------+-------+----------+----------+
| ``pychimera -i``        |   Y   |     Y    |    Y     |
+-------------------------+-------+----------+----------+
| ``pychimera -m``        |   Y   |     Y    |    Y     |
+-------------------------+-------+----------+----------+

\* In Windows, use ``python -m pychimera``, not ``pychimera``.

\*\* Only with ``qtconsole`` installed.

PyChimera has been successfully installed and tested in the following 64-bit systems:

- Linux
    + Arch Linux with UCSF Chimera 1.10, 1.11, 1.12
    + Ubuntu 14.04 with UCSF Chimera 1.10, 1.11, 1.12 (Travis CI's)
    + CentOS 6.3 with UCSF Chimera 1.11.2
- Mac OS X
    + 10.11 El Capitan with UCSF Chimera 1.12
    + 10.10 (Xcode 6.4) with UCSF Chimera 1.12 (Travis CI's)
- Windows
    + 7 SP1 with UCSF Chimera 1.12
    + Windows Server 2012 R2 with UCSF Chimera 1.12 (AppVeyor's)


.. _Travis CI: https://travis-ci.org/insilichem/pychimera
.. _AppVeyor: https://ci.appveyor.com/project/jaimergp/pychimera