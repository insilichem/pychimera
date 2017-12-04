
PyChimera
=========

.. image:: https://travis-ci.org/insilichem/pychimera.svg?branch=master
   :target: https://travis-ci.org/insilichem/pychimera
   :alt: Travis CI status

.. image:: https://ci.appveyor.com/api/projects/status/fwp3uum6be7tcfqn/branch/master?svg=true
   :target: https://ci.appveyor.com/project/jaimergp/pychimera
   :alt: AppVeyor status

.. image:: https://readthedocs.org/projects/pychimera/badge/?version=latest
   :target: http://pychimera.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation status


Use `UCSF Chimera`_ packages in any Python 2.7 interpreter.

With PyChimera you can…

-  Run scripts depending on chimera **from CLI** with ``pychimera script.py``.
-  Enable ``import chimera`` in interactive coding sessions **outside UCSF Chimera**,
   including IPython and Jupyter Notebooks.
-  Launch a standard UCSF Chimera instance, with the benefit of importing all
   your ``conda`` or ``virtualenv`` packages with ``pychimera --gui``.

Projects using PyChimera
------------------------

- `GaudiMM <https://github.com/insilichem/gaudi>`_
- `InsiliChem Plume <https://github.com/insilichem/plume>`_
- `structfit.py <https://gist.github.com/jrjhealey/a145a297f7ed4d7ea45a147347fc74b0>`_


.. toctree::
   :maxdepth: 2
   :caption: User Guide

   quickstart.rst
   install.rst
   faq.rst
   developers.rst


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Acknowledgments
---------------

Largely based on ideas by `Greg Couch at chimera-users`_.

.. _UCSF Chimera: https://www.cgl.ucsf.edu/chimera/
.. _Greg Couch at chimera-users: http://www.cgl.ucsf.edu/pipermail/chimera-users/2015-January/010647.html
