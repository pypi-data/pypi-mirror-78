*******
Roadmap
*******

The roadmap is a summary of planned changes. It is splitted into two parts:

* :ref:`Future`
* :ref:`Past`

The difference between :ref:`Past` and the :ref:`CHANGELOG` is the point of view:
:ref:`CHANGELOG` is intended for *end users* whereas :ref:`Past` is mainly for
developers.


.. _Future:

Future
======

0.4.0
-----

* [R07] Basic agent for jobs (Slurm)

  

0.5.0
-----

* [R08.2] Grafana dashboards for jobs

  

0.6.0
-----

* [R12] PerA: agent to *cook* raw data I

  * compute global metrics for the full cluster


0.7.0
-----

* [R08.3] Grafana dashboards for the full cluster

  
0.8.0
-----

* [R14] Improved sensors

  * docs: command line mechanism to get info about sensors
  * parameters: implement mechanism to pass params to sensors


0.9.0
-----

* [R01] Central management

  * OpenRC (also systemd?) script to start the system: ``fructosa``
  * ``fructosa`` starts the manager daemon ``fructosad``
  * ``fructosad`` manages ``LiMon`` and ``PerA``

    * ``LiMon`` is managed by ``lmaster`` that starts in turn the needed ``lagent``\ s
    * ``PerA`` is run by the ``perad`` daemon (?)

      
0.10.0
------

* [R13] Agent for jobs (Slurm) II

  * it can link data from slurm (jobs) to data from other agents (nodes)

  
0.11.0
------

* [R09] Automatic generation of plots for HKHLR and loewemon


0.12.0
------

* [R10] ML analysis of collected data to classify jobs (PerA)


1.0.0
-----

* [R15] Documentation

  * sensors
  * configuration files
  * command line options
  * man page
  * etc


.. _Past:

Past
====

0.2.0
-----

* [R08.1] Grafana dashboards for nodes
* Initial structure for docs
* Started using sphinx
  
  
0.3.0
-----

* [R11] Architecture's revamp I

  * heartbeat mechanism
  * agents send data directly to destination(s)


