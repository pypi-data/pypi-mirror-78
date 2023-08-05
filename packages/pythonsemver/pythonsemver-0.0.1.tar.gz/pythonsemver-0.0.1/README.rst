Python Library for Semantic Versioning
======================================

.. teaser-begin

A Python module for `semantic versioning`_. Simplifies comparing versions.

|build-status| |python-support| |downloads| |license| |docs| |black|

.. teaser-end

.. warning::

   As anything comes to an end, this project will focus on Python 3.x only.
   New features and bugfixes will be integrated into the 3.x.y branch only.

   Major version 3 of semver will contain some incompatible changes:

   * removes support for Python 2.7 and 3.3
   * removes deprecated functions.

   The last version of semver which supports Python 2.7 and 3.4 will be
   2.10.x. However, keep in mind, version 2.10.x is frozen: no new
   features nor backports will be integrated.

   We recommend to upgrade your workflow to Python 3.x to gain support,
   bugfixes, and new features.

The module follows the ``MAJOR.MINOR.PATCH`` style:

* ``MAJOR`` version when you make incompatible API changes,
* ``MINOR`` version when you add functionality in a backwards compatible manner, and
* ``PATCH`` version when you make backwards compatible bug fixes.


.. |latest-version| image:: https://img.shields.io/pypi/v/semver.svg
   :alt: Latest version on PyPI
   :target: https://pypi.org/project/semver
.. |build-status| image:: https://travis-ci.com/python-semver/python-semver.svg?branch=master
   :alt: Build status
   :target: https://travis-ci.com/python-semver/python-semver
.. |python-support| image:: https://img.shields.io/pypi/pyversions/semver.svg
   :target: https://pypi.org/project/semver
   :alt: Python versions
.. |downloads| image:: https://img.shields.io/pypi/dm/semver.svg
   :alt: Monthly downloads from PyPI
   :target: https://pypi.org/project/semver
.. |license| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :alt: Software license
   :target: https://github.com/python-semver/python-semver/blob/master/LICENSE.txt
.. |docs| image:: https://readthedocs.org/projects/python-semver/badge/?version=latest
   :target: http://python-semver.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. _semantic versioning: https://docs.npmjs.com/about-semantic-versioning
.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black Formatter
