pychimera - Use UCSF Chimera Python API in a standard interpreter
=================================================================

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
`pychimera` provides access to Chimera's modules from any Python 2.x interpreter. This is achieved
in two steps:

1. `patch_environ()` patches environment variables with proper paths (packages and libraries).
Since the original `sys.path` is exported to `PYTHONPATH`, you can use all your virtualenv/conda
packages with Chimera. This call restarts Python to inject a new `os.environ` with `os.execve`.

2. `load_chimera()` initializes Chimera. This is done through their own routines (`chimeraInit`).

You can call those two routines in your scripts to access Chimera packages.

pychimera also offers its interface through python `-m`. Add `-i` for interactive mode:

    python -[i]m pychimera [-m another_module | -c "string" | script.py | ipython | notebook]

You can also try to launch it from IPython, but some things may not work. Anyway, these two commands
have the same effect:

    pychimera ipython [notebook]
    ipython -m pychimera [notebook]

If you want to run a script with IPython and then inspect the results (`-i` flag), your best bet is
to run `pychimera ipython` and then call `%run path/to/file.py` inside the interpreter.

Notes
-----
Obviously, you need to install Chimera in your computer. `pychimera` will do its best to find the
installation path automagically in the standard locations. If somehow it doesn't succeed,
you can always set an environment variable called `CHIMERADIR` in your `.bashrc`, or similar.

    export CHIMERADIR="~/.local/UCSF-Chimera"

Acknowledgments
---------------
Largely based on ideas by [Greg Couch at chimera-users](http://www.cgl.ucsf.edu/pipermail/chimera-users/2015-January/010647.html).