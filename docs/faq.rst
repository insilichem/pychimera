FAQ & Known issues
==================

Numpy problems
--------------

UCSF Chimera bundles its own distribution of some popular packages, like
``numpy``, and those are loaded before your env packages for compatibility
reasons. Be warned if you use specific versions for your project,
because you can face strange bugs if you don’t take this into account.

For example:

::

    RuntimeError: module compiled against API version 9 but this version of numpy is 7

In some platforms (Linux), this can be worked around with some work on
the precendence of paths in ``sys.path``, but in some of them is not as easy (OS X).
The easiest and most robust way to fix this is by upgrading UCSF Chimera's ``numpy``:

::

    pip install --upgrade numpy -t "$(pychimera --path)/lib/python2.7/site-packages"

Take into account that this action will prevent outdated extensions from working again. As a far as we know, these are affected, but there might be more (please report it so we can update this list!):

- MMTK-dependent extensions: MD, Energy minimization
- AutoDock-dependent extensions: AutoDock Vina

If you use those often enough, you should have a separate, unmodified UCSF Chimera installation.

PyChimera GUI has ugly fonts
----------------------------

Anaconda-provided ``tk`` package is not built with truetype support (for several reasons; read `here <https://github.com/ContinuumIO/anaconda-issues/issues/776>`_ and `here <https://github.com/ContinuumIO/anaconda-issues/issues/6833>`_). Chimera does ship its own one (with correct font support), but since PyChimera loads its own Python interpreter, it ends up being replaces with ``conda``'s one. All ``conda`` environments are created with ``tk`` by default, so if the fonts really bother you, you can uninstall it with ``conda remove --force tk`` and it will fallback to system's one if needed.

Setuptools problems
-------------------

If you are using the development versions of ``pychimera``, Chimera's ``setuptools`` will
complain about the versioning scheme (ie, ``pychimera==0.1.11+6.gc2e1fbb.dirty``). As before,
the fix is to upgrade the package. You might have to remove it manually beforehand, though:

::

    rm -r $(pychimera --path)/lib/python2.7/site-packages/setuptools-3.1*
    pip install --upgrade setuptools -t "$(pychimera --path)/lib/python2.7/site-packages"

Chimera reports problems with libgfxinfo.so and pcrecpp
-------------------------------------------------------

The error traceback ends with:

::

    libgfxinfo.so: undefined symbol: _ZN7pcrecpp2RE4InitERKSsPKNS_10RE_OptionsE

This is due to an incompatibility between Chimera's ``pcre`` libraries and those loaded by PyChimera. Depending on how you installed PyChimera, these will be:

- Installed with ``conda`` (or with ``pip`` but inside a ``conda`` environment): the libraries will correspond to the ``pcre`` package in the conda environment. To make sure it works, you would probably have to downgrade to version 8.39 with ``conda install pcre=8.39``.
- Installed with ``pip`` (outside a conda environment): the loaded library will be the system's one. If you can afford to downgrade to version 8.39 system-wide, do it. You will probably not, so the best option is to create a ``conda`` environment to execute PyChimera properly: ``conda create -n pychimera -c insilichem pychimera``.
- If nothing else works, you can try (as a last resort!) to remove the ``pcre`` package altogether. This can have some unexpected side effects in your environment, but if you only installed one of our projects (e.g. ``gaudi``), you should be fine. Do it like this: ``conda remove --force pcre``.

dateutil version
----------------

As Numpy, the ``dateutil`` version shipped with Chimera is old, which can cause problems with some modern libaries. The solution is the same: upgrade the package built in Chimera.

::

    pip install -U -t $(pychimera --path)/lib/python2.7/site-packages python-dateutil
