========
Overview
========

Market Mix Modeling

* Free software: GNU Lesser General Public License v3 or later (LGPLv3+)

Installation
============

::

    pip install mrktmix

You can also install the in-development version with::

    pip install git+ssh://git@market_mix_model/apd_540@hotmail.com/market_mix_model.git@master

Documentation
=============


https://mrktmix.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
