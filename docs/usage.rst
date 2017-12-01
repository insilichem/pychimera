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


To execute a script:

::

    pychimera script.py

To launch Chimera GUI with custom packages:

::

    pychimera --gui


To launch a module that uses Chimera internally:

::

    pychimera -m this

To execute any Python statement:

::

    pychimera -c 'import chimera'


.. _multiplatform:

Multiplatform compatibility matrix
----------------------------------

UCSF Chimera is available for Linux, Mac OS X and Windows. PyChimera does its best to provide the same compatibility for all three platforms and each release is continuously tested in Travis CI (Linux, Mac OS X) and AppVeyor (Windows). Despite our efforts, some features might not be as polished in some platforms. The table below summarizes the current state of implementation:

+-------------------------+-----------------------------+
|                         | Platforms                   |
+       Features          +-------+----------+----------+
|                         | Linux | Mac OS X | Windows* |
+=========================+=======+==========+==========+
| ``pychimera``           |   Y   |     Y    |    N     |
+-------------------------+-------+----------+----------+
| ``pychimera script.py`` |   Y   |     Y    |    Y     |
+-------------------------+-------+----------+----------+
| ``pychimera ipython``   |   Y   |     Y    |    Y^    |
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

- \* In Windows, you have to run ``python -m pychimera`` instead of ``pychimera``.
- ^ Only with ``qtconsole`` installed.