PyChimera
=========

.. image:: https://travis-ci.org/insilichem/pychimera.svg?branch=master
   :target: https://travis-ci.org/insilichem/pychimera

.. image:: https://ci.appveyor.com/api/projects/status/fwp3uum6be7tcfqn/branch/master?svg=true
   :target: https://ci.appveyor.com/project/jaimergp/pychimera

.. image:: https://zenodo.org/badge/50309940.svg
   :target: https://zenodo.org/badge/latestdoi/50309940


Use `UCSF Chimera`_ packages in any Python 2.7 interpreter

With PyChimera you can…

-  Run scripts depending on chimera **from CLI** with ``pychimera``.
-  Enable ``import chimera`` in interactive coding sessions (console, ipython)
   **outside Chimera**.
-  Use Jupyter Notebooks with Chimera. You only need to run the prepopulated cell.
-  Launch a standard Chimera instance, with the benefit of importing all
   your conda or virtualenv packages with ``pychimera --gui``.

I hope it’s useful! Feedback is appreciated!


Acknowledgments
---------------

Largely based on ideas by `Greg Couch at chimera-users`_.

.. _UCSF Chimera: https://www.cgl.ucsf.edu/chimera/
.. _latest UCSF Chimera: http://www.cgl.ucsf.edu/chimera/download.html
.. _Greg Couch at chimera-users: http://www.cgl.ucsf.edu/pipermail/chimera-users/2015-January/010647.html


Citation
--------

.. image:: https://zenodo.org/badge/50309940.svg
   :target: https://zenodo.org/badge/latestdoi/50309940

PyChimera is scientific software, funded by public research grants
(Spanish MINECO's project ``CTQ2014-54071-P``, Generalitat de Catalunya's
project ``2014SGR989`` and research grant ``2015FI_B00768``, COST Action ``CM1306``).
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