========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/helpertools/badge/?style=flat
    :target: https://readthedocs.org/projects/helpertools
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/helpertools/helpertools.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/helpertools/helpertools

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/helpertools/helpertools?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/helpertools/helpertools

.. |requires| image:: https://requires.io/github/helpertools/helpertools/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/helpertools/helpertools/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/helpertools/helpertools/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/helpertools/helpertools

.. |version| image:: https://img.shields.io/pypi/v/helpertools.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/helpertools

.. |wheel| image:: https://img.shields.io/pypi/wheel/helpertools.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/helpertools

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/helpertools.svg
    :alt: Supported versions
    :target: https://pypi.org/project/helpertools

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/helpertools.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/helpertools

.. |commits-since| image:: https://img.shields.io/github/commits-since/helpertools/helpertools/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/helpertools/helpertools/compare/v0.0.0...master



.. end-badges

helper tools for python

* Free software: Apache Software License 2.0

Installation
============

::

    pip install helpertools

You can also install the in-development version with::

    https://github.com/sandeepsn1997/helpertools/blob/master/README.rst

Documentation
=============


https://helpertools.readthedocs.io/


Development
===========

To run the all tests run::

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
