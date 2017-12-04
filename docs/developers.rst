For developers
==============

Quick API
---------

PyChimera provides access to UCSF Chimera’s modules from any Python 2.x
interpreter. This is achieved in two steps:

1. ``patch_environ()`` patches environment variables with proper paths
   (packages and libraries). Since the original ``sys.path`` is exported
   to ``PYTHONPATH``, you can use all your virtualenv/conda packages
   with Chimera. This call restarts Python to inject a new
   ``os.environ`` with ``os.execve``.

2. ``enable_chimera()`` initializes Chimera. This is done through their
   own routines (``chimeraInit``).

As a result, if you want to use PyChimera in your developments, you only need
to execute these lines at the beginning of the script. For example, PyChimera
is used programmatically in the `GaudiMM`_ CLI entry point.


::

    import pychimera
    pychimera.patch_environ()
    pychimera.enable_chimera()


Calling ``patch_environ()`` will result in the interpreter being restarted
to inject all UCSF Chimera libraries; take that into account in the logic
of your program. This is why you should probably add the lines at the very
beginning of the script.

Alternatively, you can leave those lines out and have your users execute
the script with ``pychimera`` instead of ``python``. Up to you, but usually
you will prefer to hide the technical details...


Alternative methods
-------------------

PyChimera also offers its interface through python ``-m``. This has not
been thoroughly tested, so it may not work perfectly. Add ``-i`` for interactive mode:

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


.. _GaudiMM: https://github.com/insilichem/gaudi/blob/master/gaudi/cli/gaudi_cli.py#L71


How does it work?
-----------------

When you run ``patch_environ``, we try to locate a valid UCSF Chimera installation
in the system. This is performed with three alternative strategies:

1. Check if a ``CHIMERADIR`` variable is set. This is normally set by the user when the
   automated strategies can't work right due to the system configuration. If the path
   is valid, use that as the UCSF Chimera installation directory. Else, try strategy #2.
2. Check if an executable called ``chimera`` is somewhere in ``PATH``. This is done with
   ``disutils.spawn.find_executable``. If successful, figure out the UCSF Chimera installation
   directory from the file path after resolving any possible symlinks.
3. If ``chimera`` is not in ``PATH``, we can try to find the installation directory in
   the default locations (``~/.local`` or ``/opt`` for Linux, ``/Applications`` for Mac OS X,
   ``C:\Program Files`` for Windows).

Once we have located a valid UCSF Chimera, we find the needed libraries and Python modules
to patch ``LD_LIBRARY_PATH``, ``PYTHONPATH`` and other environment variables, as specified
in their `own shell launcher`_ (Linux/OSX) and `cpp launcher`_ (Windows). In this step,
any additional packages and libraries installed in a ``conda`` environment or ``virtualenv``
are also injected. For all this to work, the interpreter is restarted.

After the restart, ``enable_chimera`` is called, which runs the UCSF Chimera initialization
routines contained in ``chimeraInit.py``. Depending on the CLI options, we then run a script,
run IPython/Notebook or start the GUI.

.. _own shell launcher: http://plato.cgl.ucsf.edu/trac/chimera/browser/trunk/apps/common-unix
.. _cpp launcher: http://plato.cgl.ucsf.edu/trac/chimera/browser/trunk/apps/chimera/launcher/launcher.cpp