=============================
Dynamic Flux Balance Analysis
=============================

.. image:: https://img.shields.io/pypi/v/dfba.svg
   :target: https://pypi.org/project/dfba/
   :alt: Current PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/dfba.svg
   :target: https://pypi.org/project/dfba/
   :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/dfba.svg
   :target: http://www.gnu.org/licenses/
   :alt: GPLv3+

.. image:: https://gitlab.com/davidtourigny/dynamic-fba/badges/master/pipeline.svg
   :target: https://travis-ci.org/davidtourigny/dynamic-fba/commits/master
   :alt: Pipeline Status

.. image:: https://gitlab.com/davidtourigny/dynamic-fba/badges/master/coverage.svg
   :target: https://gitlab.com/davidtourigny/dynamic-fba/commits/master
   :alt: Coverage Report

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Black

.. _`Harwood et al., 2016`: https://link.springer.com/article/10.1007/s00211-015-0760-3
.. _GLPK: https://www.gnu.org/software/glpk/
.. _SUNDIALS: https://computation.llnl.gov/projects/sundials
.. _Python: https://www.python.org/
.. _cobrapy: https://github.com/opencobra/cobrapy
.. _optlang: https://github.com/biosustain/optlang
.. _symengine: https://github.com/symengine/symengine

This project provides an object-oriented software package for dynamic
flux-balance analysis (DFBA) simulations using implementations of the direct
method or Algorithm 1 described in the paper `Harwood et al., 2016`_. The main
algorithms for solving embedded LP problems are written in *C++* and use the GNU
Linear Programming Kit (GLPK_) and the Suite of Nonlinear and
Differential/Algebraic Equation Solvers (SUNDIALS_) CVODE or IDA. Extension
modules to cobrapy_ are provided for easy generation and simulation of DFBA
models.

Installation
============

.. _GLPK: https://www.gnu.org/software/glpk/
.. _SUNDIALS: https://computation.llnl.gov/projects/sundials
.. _Python: https://www.python.org/
.. _cobrapy: https://github.com/opencobra/cobrapy
.. _optlang: https://github.com/biosustain/optlang
.. _symengine: https://github.com/symengine/symengine

Currently, we do not provide Python wheels for this package and therefore `Installing from
source`_ is a bit more involved. The quickest way to run the software
is from the provided `Docker <https://docs.docker.com/>`_ image:

.. code-block:: console

    docker run --rm -it davidtourigny/dfba:latest


Installing from source
----------------------

Currently this package is compatible with most UNIX-like operating systems.
Provided the following `Dependencies`_ are installed, the module
can be installed from the root of the repository using the command:

.. code-block:: console

    pip install .

Dependencies
~~~~~~~~~~~~

.. _`build_glpk.sh`: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/scripts/build_glpk.sh
.. _`build_pybind11.sh`: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/scripts/build_pybind11.sh
.. _`build_sundials.sh`: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/scripts/build_sundials.sh
.. _Dockerfile: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/Dockerfile
.. _`pybind11`: https://github.com/pybind/pybind11


* A version of Python_ 3.6 or higher is required
* You need `cmake <https://cmake.org/>`_ for the build process
* You will need `git <https://git-scm.com/>`_ to clone this repository to access
  the scripts and build files
* You need a working compiler with C++11 support, for example, by installing
  ``build-essential`` on Debian-derived Linux systems
* GLPK_ version 4.65 is required or can be installed using `build_glpk.sh`_
* SUNDIALS_ version 5.0.0 or higher is required or can be installed using `build_sundials.sh`_
* pybind11_ is required or can be installed using `build_pybind11.sh`_

Be aware that some of these packages have their own dependencies that must
therefore be installed also (e.g. GLPK_ depends on `GMP <https://gmplib.org/>`_
and pybind11_ requires `pytest <https://docs.pytest.org/en/latest/>`_).


Alternatively, a Dockerfile_ is provided for building a `Docker <https://docs.docker.com/>`_
image to run the software from an interactive container. The `Docker <https://docs.docker.com/>`_ image can be
built in one step by issuing the command:

.. code-block:: console

    make build

from the root of this repository. It can then be started using:

.. code-block:: console

    make run

Documentation
=============

Documentation for dfba is provided at `readthedocs <https://dynamic-fba.readthedocs.io>`_

Authors
=======

* David S. Tourigny
* Moritz E. Beber

Additional contributors
=======================

* Jorge Carrasco Muriel (visualization and documentation)

Funding
=======

* David S. Tourigny is a Simons Foundation Fellow of the Life Sciences Research
  Foundation.

Copyright
=========

* Copyright © 2018,2019 Columbia University Irving Medical Center, New York, USA
* Copyright © 2019 Novo Nordisk Foundation Center for Biosustainability,
  Technical University of Denmark
* Free software distributed under the `GNU General Public License v3 or later
  (GPLv3+) <http://www.gnu.org/licenses/>`_.
