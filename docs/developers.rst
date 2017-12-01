For developers
==============

PyChimera provides access to Chimera’s modules from any Python 2.x
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

Additionally, you can have your users execute the script with ``pychimera``
instead of ``python``. Up to you, but usually you will prefer to hide the
technical details...


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