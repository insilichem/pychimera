FAQ & Known issues
==================

1. ``pychimera --gui``

UCSF Chimera bundles its own distribution of some popular packages, like
numpy, and those are loaded before your env packages for compatibility
reasons. Be warned if you use specific versions for your project,
because you can face strange bugs if you don’t take this into account.

In some platforms (Linux), this can be worked around with some work on
the precendence of paths in ``sys.path``, but in some of them is not as easy (OS X).
The easiest and most robust way to fix this is by upgrading Chimera's ``numpy``:

::

    pip install --upgrade numpy -t `pychimera --path`/lib/python2.7/site-packages

Take into account that this action will prevent MMTK extensions from working again.
If you use those often enough, you can have a separate, unmodified UCSF Chimera installation.


If you are using the development versions of ``pychimera``, Chimera's ``setuptools`` will complain
about the versioning scheme (ie, ``pychimera==0.1.11+6.gc2e1fbb.dirty``). As before,
the fix is to upgrade the package. You might have to remove it manually beforehand, though:

::

    rm -r `pychimera --path`/lib/python2.7/site-packages/setuptools-3.1*
    pip install --upgrade setuptools -t `pychimera --path`/lib/python2.7/site-packages
