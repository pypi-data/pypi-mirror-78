#################
Development notes
#################


***********************
HOWTO release a version
***********************

1. Ensure that the tests pass: ``tox``
2. Update ``CHANGELOG.rst`` and ``docs/development/roadmap.rst``
3. Update ``README.rst`` if needed
4. Update version::

     $ bump2version <type>

   where ``<type>`` is ``major``, ``minor`` or ``patch``.
   
   OLD:
     before, using scm_version, it used to be like follows

     Make a tag: ``hg tag ...``
     
5. Make a source distribution and a wheel::

     $ python setup.py sdist bdist_wheel

6. Upload the generated files to PyPI::

     $ twine upload dist/...tar.gz dist/...py3-non-any.whl

7. Update project's homepage, if needed.

   
**************
Some decisions
**************

Structure of code
=================

* ``fructosad.py``, ``lagent.py`` and ``lmaster.py`` contain code to trivially create executables
  via their main functions.


Functional Tests
================

In general, it is expected that ``lmaster`` and ``lagent`` (and other executables in the package)
run with privileges. Therefore to isolate and limit the impact of the functional tests on the
host, it was decided to run the daemons for FTing inside containers.

This behaviour can be controlled with an environment varaible called ``FRUCTOSA_FT_ENVIRONMENT``.

* Setting ``FRUCTOSA_FT_ENVIRONMENT=docker`` (default) makes the FTs run the programs under
  test inside docker containers.
* With ``FRUCTOSA_FT_ENVIRONMENT=host`` the FTs run directly in the host.
* The location of the project need to be set somehow to install it in the containers. This
  can be controlled with an environment variable: ``FRUCTOSA_PROJECT_PATH``.
  If unset, the location is inferred from the location of the ``environment.py`` file
  (which lives in ``tests/functional/``).


How to run the Functional Tests (FTs)
-------------------------------------

In ``devel`` there are some dockerfiles that can be used to create the images
needed to run the FTs inside containers. For instance::

  $ cd devel/
  $ docker build --tag fructosa:py37 -f FrUCToSA-dev-py37.df .

optionally one could set additional tags::
  
  $ docker build --tag fructosa:py37 --tag fructosa:auto --tag fructosa:latest -f FrUCToSA-dev-py37.df .

With that, the FTs should run smothly (hopefully!) with::

  (python-3.7) $ pytest tests/functional/

Or with::

  $ tox
  $ # or
  $ tox -e py37-functional

  
Unit Tests
==========

Each line of actual production code is expected to be covered by unit tests.


How to run the Unit Tests (UTs)
-------------------------------

The unit tests can be run with::

  (python-3.7) $ pytest tests/unit

or with::

  $ tox -e py37-unit
  

Doctests
========

Straightforward UTs can be written in the docstring of the given unit. This serves
two purposes:

1. It simplifies UTs
2. It serves as documentation, as docstrings are typically easier to read than
   UTs

How to run the Doctests
-----------------------

The doctests can be run with::

  (python-3.7) $ pytest fructosa

or with::

  $ tox -e py37-doctest
  



How to run the Unit Tests (UTs)
-------------------------------

The unit tests can be run with::

  (python-3.7) $ pytest tests/unit

or with::

  $ tox -e py37-unit
  

****************
Daemon processes
****************

* typically accept command line options for

  * configuration file
  * logging file/directory
  * pidfile (?)
    
* general logging messages to a specific log file (like ``/var/log/fructosad.log``); errors
  go to syslog (``/var/log/syslog``) -- done anyway by the Linux logging system
* Catch SIGHUP to allow re-reading of configuration
  

**************************
File locking and PID files
**************************

Ref. [Rago2013]_, pag. 473 (see also p. 494 for a definition of the ``lockfile`` function)
explains how to create a locked PID file.

Probably better explained can be found in ref. [Kerrisk2010]_, page 1142. The code for
``lockRegion`` can be found on page 1134.

In Python, one can use ``os.lockf``. See the docs. The meaning of the possible values for
``cmd`` can be seen with ``man 3 lockf``. Also the other parameters are explained, of course.


**********************
AsyncIO and unit tests
**********************

A simple approach is described by Miguel Grinberg in his blog:
https://blog.miguelgrinberg.com/post/unit-testing-asyncio-code
I implemented my own version of his _run and AsyncMock in
``test/unit/fructosa/aio_tools.py``.


************
Bibliography
************

[Rago2013] R. Stevens, S. Rago "Advanced Programming in the UNIX Environment", 3rd ed.
  Addison Wesley, 2013

[Kerrisk2010] M. Kerrisk, "The Linux Programming Interface", No Starch Press Press, 2010
