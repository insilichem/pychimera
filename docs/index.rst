
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

.. image:: https://zenodo.org/badge/50309940.svg
   :target: https://zenodo.org/badge/latestdoi/50309940
   :alt: Zenodo DOI


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

Citation
--------

PyChimera is scientific software, funded by public research grants
(Spanish MINECO's project ``CTQ2014-54071-P``, Generalitat de Catalunya's
project ``2014SGR989`` and research grant ``2017FI_B2_00168``, COST Action ``CM1306``).
If you make use of PyChimera in scientific publications, please cite it. It will help
measure the impact of our research and future funding!

.. code-block:: latex

    @misc{jaime_rgp_2017_546883,
      author       = {Jaime Rodríguez-Guerra Pedregal and
                      Jean-Didier Maréchal},
      title        = {insilichem/pychimera: PyChimera},
      month        = apr,
      year         = 2017,
      doi          = {10.5281/zenodo.546883},
      url          = {https://doi.org/10.5281/zenodo.546883}
    }

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
