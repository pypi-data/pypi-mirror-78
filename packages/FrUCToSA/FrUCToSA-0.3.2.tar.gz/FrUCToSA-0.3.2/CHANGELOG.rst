*********
Changelog
*********

What *high level* changes are included in each published version.


0.3.1
=====

* Sensors follow a more strict mechanism for metric naming hierarchy:
  {hostname (without dots)}.{sensor name}


0.3.0
=====

* Heartbeat mechanism implemented: ``lagent`` is the source and ``lmaster``
  the sink.
* Data from sensors is now directly sent to ``Graphite`` from ``lagent``.

  
0.2.0
=====

* Added executable ``make-fructosa-dashboard`` to generate Grafana dashboards.
* Documuentation improved

  * roadmap
  * deployment
  * architecture
  * development
    
* [devel] CL options factorized out from main conf class:

    ``FructosaDConf`` -> ``FructosaDConf`` + ``CLConf``

  This change should be transparent for customers of the ``FructosaDConf`` class.
  

0.1.0
=====

* migrated from QULo_
* [testing:FTs] The location of the project can be controlled with an environment
  variable: ``FRUCTOSA_PROJECT_PATH``, if unset, the location is inferred from
  the location of the ``environment.py`` file (which lives in ``tests/functional/``).
  This feature is needed to create the docker compose files neceessary to run
  the FTs inside containers.

.. _QULo: https://itp.uni-frankfurt.de/~palao/software/QULo/
