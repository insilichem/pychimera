Installation
============

PyChimera is a wrapper around UCSF Chimera, so it makes sense that you have
to install it beforehand. Additionally, to reduce compatibility problems,
PyChimera is best used within a ``conda`` environment.

Recommended steps
-----------------

1. Install Miniconda
....................

Anaconda is a Python distribution that bundles all the scientific packages
you will ever need. It also provides a fancy package manager to update and
install more if you need it. A stripped-down version of Anaconda that only
includes the package manager (``conda``) and the essential Python packages,
called Miniconda, is also available and it's the one we will use here.

Go the `Miniconda`_ webpage and download the installer for your platform. For
the sake of simplicity, choose the Python 2.7 version. You can use the 3.6
version if you really want, but you will need to create a Python 2.7
environment later.

Once you have downloaded the installer, run it. Depending on the platform,
you have to do it differently.

**Linux and Mac OS X**

Just run ``bash ~/Downloads/Miniconda*.sh`` and follow the wizard. Make
sure to answer yes when the installer asks about modifying your ``.bashrc``.
When you are done, close the terminal and reopen it to apply the changes.

**Windows**

Double-click on the .exe and follow the steps. Make sure to add Miniconda
to your %PATH% when you are asked about it.

2. Install UCSF Chimera
.......................

First, if you haven’t already, install UCSF Chimera. If you already
have it installed, skip to step 2, but make sure you satisfy the requirements
detailed in step 4.

PyChimera has been tested on UCSF Chimera 1.10 and above on Linux, Mac OS X and Windows.
See :ref:`multiplatform` for more details. Go to the `UCSF Chimera download`_
page and get the latest installer for your platform (1.12 at the time of writing).
You probably want the 64bit version.

Once you have it in disk, run it. Depending on the platform, this is performed differently:

**Linux**

You need to run these commands in a terminal:

::

    cd ~/Downloads  # or whatever it is in your system
    chmod +x chimera*.bin
    ./chimera*.bin

At the final step, you will be asked to create a symlink in one of the places specified
in your $PATH. Choose the one that refers to the Miniconda installation.

**Windows**

Just double click on the .exe and follow the steps of the installation wizard.

3. Install PyChimera
....................

With ``conda`` and UCSF Chimera in your system, this step is really easy!

::

    conda install -c insilichem pychimera

If you installed Miniconda 3.6 or want to use a separate environment, use these ones:

::

    conda create -n pychimera -c insilichem python=2.7 pychimera
    source activate pychimera  # Linux and Mac OS x
    activate pychimera  # Windows only

4. Make sure ``chimera`` can be found
.....................................

If you followed all the steps, you should be able to run ``pychimera --path`` and obtain
the UCSF Chimera installation directory as a result. However, if you used a different
installation path and did not symlink the binary to somewhere in your PATH, ``pychimera``
won't be able to locate it. There's a workaround for this! Just set an environment variable
called ``CHIMERADIR`` pointing to the UCSF Chimera installation directory.

In Linux and Mac OS X, this can be done in your ``.bashrc`` or equivalent.

::

    export CHIMERADIR="~/.local/UCSF-Chimera"

In Windows, you have to search "Environment variables" in the Start menu and create a new
user environment variable in the popup dialog. Remember, the variable name is ``CHIMERADIR``
and the value should be something like ``C:\Program Files\Chimera 1.12``.


Alternative procedure
---------------------

If you don't want (or can't) use ``conda``, you can also install PyChimera with ``pip``:

::

    pip install pychimera

or directly from source:

::

    # With git
    git clone https://github.com/insilichem/pychimera.git && python pychimera/setup.py install

    # With wget
    wget https://github.com/insilichem/pychimera/archive/master.zip
    unzip pychimera*.zip
    python pychimera-master/setup.py install

While this *should* work in an ideal environment, it would probably have some rough edges
due to the libraries installed in your system being different than the ones provided by
UCSF Chimera. The ``pychimera`` conda package has been finetuned to work with the correct
versions so, if possible use that. Otherwise, refer to the `conda recipe`_ to identify
the correct versions.


.. _ExtraPackages:

Extra packages
--------------

So far, you have a barebones ``pychimera`` installation. If you want to make use of all
the Jupyter compatibility features, you will need to install some extra packages. Namely:

::

    # First, activate your environment if necessary
    # source activate pychimera
    conda install ipython jupyter notebook
    # In Windows, you will also need:
    conda install qtconsole
    # For interactive visualization in the notebook:
    conda install -c bioconda nglview
    # might need: jupyter-nbextension enable nglview --py --sys-prefix

.. _UCSF Chimera: https://www.cgl.ucsf.edu/chimera/
.. _Greg Couch at chimera-users: http://www.cgl.ucsf.edu/pipermail/chimera-users/2015-January/010647.html
.. _UCSF Chimera download: https://www.cgl.ucsf.edu/chimera/download.html
.. _conda: https://conda.io/miniconda.html
.. _Miniconda: https://conda.io/miniconda.html
.. _conda recipe: https://github.com/insilichem/pychimera/blob/master/conda-recipes/pychimera/meta.yaml
