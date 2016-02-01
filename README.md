PyChimera
=========

Use [UCSF Chimera](https://www.cgl.ucsf.edu/chimera/) packages in any Python 2.7 interpreter 

With PyChimera you can...

* Enable `import chimera` in interactive coding sessions (console, notebooks) __outside Chimera__. 
Just call `enable_chimera()`. _Careful! Call it prior to other code or you'll lose your previous work._
* You can also launch Chimera-preenabled IPython sessions or Notebooks with `pychimera ipython` and 
`pychimera notebook` respectively.
* Run scripts depending on chimera __from CLI__ with either `pychimera` or `python -m chimera`. This 
includes modules (`-m` flag) and strings (`-c` flag).

I hope it's useful! Feedback is appreciated!

Installation
------------
First, if you haven't already, install [latest UCSF Chimera](http://www.cgl.ucsf.edu/chimera/download.html).

Then, install PyChimera via `pip`, `conda` or `setup.py`:

    pip install pychimera
    conda install -c insilichem pychimera
    git clone https://github.com/insilichem/pychimera.git && python pychimera/setup.py install

Usage
-----
Run `pychimera -h` for quick help.

To start an interactive Python session:

    pychimera                  # standalone
    pychimera -i some_file.py  # with some file
    pychimera -im module       # with a Python module
    pychimera -ic "string"     # with a command
    pychimera ipython          # launch IPython interpreter
    pychimera notebook         # launch IPython notebook

To launch a module that uses Chimera internally:

    pychimera -m this

To execute any Python statement:

    pychimera -c 'import chimera'

To execute one or more scripts:

    pychimera script.py [script_2.py ...]


For developers
--------------
PyChimera provides access to Chimera's modules from any Python 2.x interpreter. This is achieved
in two steps:

1. `patch_environ()` patches environment variables with proper paths (packages and libraries).
Since the original `sys.path` is exported to `PYTHONPATH`, you can use all your virtualenv/conda
packages with Chimera. This call restarts Python to inject a new `os.environ` with `os.execve`.

2. `load_chimera()` initializes Chimera. This is done through their own routines (`chimeraInit`).

However, you may call the alias function `enable_chimera()` without worrying on the steps.

PyChimera also offers its interface through python `-m`. Add `-i` for interactive mode:

    python -[i]m pychimera [-m another_module | -c "string" | script.py | ipython | notebook]

You can also try to launch it from IPython, but some things may not work. Anyway, these two commands
have the same effect:

    pychimera ipython [notebook]
    ipython -m pychimera [notebook]

If you want to run a script with IPython and then inspect the results (`-i` flag), your best bet is
to run `pychimera ipython` and then call `%run path/to/file.py` inside the interpreter.

Notes
-----
Obviously, you need to install Chimera in your computer. PyChimera will do its best to find the
installation path automagically in the standard locations. If somehow it doesn't succeed,
you can always set an environment variable called `CHIMERADIR` in your `.bashrc`, or similar.

    export CHIMERADIR="~/.local/UCSF-Chimera"

Chimera bundles its own distribution of some popular packages, like numpy, and those are loaded before
your env packages for compatibility reasons. Be warned if you use specific versions for your project,
because you can face strange bugs if you don't take this into account.

Acknowledgments
---------------
Largely based on ideas by [Greg Couch at chimera-users](http://www.cgl.ucsf.edu/pipermail/chimera-users/2015-January/010647.html).