********************
The FrUCToSA package
********************

Warning!
========

.. figure:: devel/in-progress-icon-2.jpg
    :width: 200px
    :align: center
    :height: 200px
    :alt: work in progress
    :figclass: align-center

    **This is work in progress!**

    Some features marked with **Warning: TBD!** are not yet developed.


Introduction
============

**FrUCToSA** stands for **Fr**\ ankfurt **U**\ niversity **C**\ luster **T**\ ool **o**\ f
**S**\ oftware **A**\ nalysis.

It is a simple tool to

1. collect, and
2. analyze

data from software running on a cluster (like Goethe-HLR_) ---and from the cluster itself---
and to analyze that data with performance "in mind".


**FrUCToSA** is made of two elements:

* **LiMon**: a **Li**\ ght **Mon**\ itor that collects data.
* **PerA**: a **Per**\ formance **A**\ nalyzer that analyzes the data and
  classifies it.  **Warning: TBD!**

The package provides several programs:

* ``fructosad``: main program. It works in the background (as a service/daemon) orchestrating
  all the system. **Warning: TBD!**
* ``lagent``: ``LiMon`` agent. Customizable service/daemon that collects performance data
  from the a node on the cluster. It runs locally and collects data from sensors that can be
  activated and configured via a configuration file.
* ``lmaster``: ``LiMon`` master. Another service/daemon that controls the agents and collects
  data from them. It runs in a master node of the cluster; it is controled via a configuration
  file.
* ``perad``: another service/daemon that analyzes the data and classifies it according to
  the performance  **Warning: TBD!**
* ``make-fructosa-dashboard``: to generate Grafana dashboards.

**FrUCToSA** is developed in Python at the CSC_ (Goethe Universitaet Frankfurt) under the
GPL3 license.


.. _Goethe-HLR: https://csc.uni-frankfurt.de/
.. _CSC: Goethe-HLR_

  
Installation
============
   
Just install the FrUCToSA package from PyPI: ::

  $ pip install FrUCToSA


  
Usage
=====

1. Configure ``lmaster`` and ``lagent``
2. [optional] Start Graphite (the data will be sent to it)
3. [optional] Start Grafana and connect it to Graphite: this is an easy way to have
   nice plots and dashboards.
4. Start ``lmaster`` (see the output of ``lmaster -h``, to learn about some parameters
   to control ``lmaster``)::

      # lmaster start

   A configuration file is needed. By default the configuration file is
   ``/etc/fructosa/lmaster.conf`` but that can be changed from the command line.

   A typical configuration might be::

      [lmaster]
      host = localhost
      incoming data port = 7888
      
      [logging]
      filename = /tmp/limon.log
      maxBytes = 1073741824
      backupCount = 10
      level = DEBUG

   No option is mandatory. In the file ``fructosa/constants.py`` the defaults are defined.
   
5. Start ``lagent`` on one or several computers (again, see the output of ``lagent -h``,
   for more details)::

      # lagent start

   A configuration file is needed. By default the configuration file is
   ``/etc/fructosa/lagent.conf``, but can be changed from the command line.
   In this configuration file is where the needed *sensor*\ s are activated.
   A typical configuration with the master and the agent running locally
   looks like this::
      
      [lmaster]
      host = localhost
      incoming data port = 7888

      [Graphite]
      host = localhost
      carbon receiver pickle port = 2004
      
      [logging]
      filename = /tmp/limon.log
      maxBytes = 1073741824
      backupCount = 10
      level = DEBUG

      [sensor:CPUPercent]
      time_interval = 10
      
      [sensor:VirtualMemory]
      time_interval = 30
      
      [sensor:CPUTimes]
      time_interval = 30
      
      [sensor:CPUTimesPercent]
      time_interval = 10
      
      [sensor:CPUCount]
      time_interval = 300
      
      [sensor:CPUStats]
      time_interval = 30
      
      [sensor:CPUFreq]
      time_interval = 300
      
      [sensor:SwapMemory]
      time_interval = 60
      
      [sensor:DiskPartitions]
      time_interval = 60
      
      [sensor:DiskUsage]
      time_interval = 30
      #path = /
      
      [sensor:DiskIOCounters]
      time_interval = 20
      
      [sensor:NetIOCounters]
      time_interval = 10
      
      [sensor:NetConnections]
      time_interval = 20
      
      [sensor:NetIFAddrs]
      time_interval = 30
      
      [sensor:NetIFStats]
      time_interval = 30
      
      [sensor:SensorsTemperatures]
      time_interval = 30
      
      [sensor:SensorsFans]
      time_interval = 30
      
      [sensor:SensorsBattery]
      time_interval = 30
      
      [sensor:BootTime]
      time_interval = 300
      
      [sensor:Users]
      time_interval = 10

   This is just an example with many sensors active. No option is mandatory. But if ``lagent``
   must measure anything, some sensor must be explicitly given. In the file
   ``fructosa/constants.py`` the defaults are defined.
   The *time* given in the ``time_interval`` option is understood to be in *seconds*.
   If the agent runs on a different computer as the master, the ``host`` entry in the
   ``lmaster`` section must be adjusted accordingly.


Security
========

All the communications between ``lmaster`` and ``lagent`` are *bona fide*. There are
no authentication or encryption mechanisms for now.
   

TODO
====

* Change ``constants.py``: ``lagent``, ``lmaster`` -> ``limon``
* ``lagent`` should have an option to display the available sensors and some help for each sensor.
* Sensors should accept options: the mechanism is almost there, but need to be completed.
* Add sensors to read data from GPUs.
* Connect to Slurm.  
* Add configuration options to manage ``Graphite``:

  * send data to it or not? (yes by default)

* openrc scripts to manage the whole system:

  * *start* 

    1. start graphite
    2. start grafana (?)
    3. start lmaster
    4. start lagents where needed

  * *stop*

    1. stop lagents
    2. stop lmaster
    3. stop grafana (?)
    4. stop graphite

  * *restart*
  * ``/etc/conf.d/fructosa`` with info about *what* to do.
  * ``/etc/fructosa/fructosa.conf`` with info about *how* to do.

* Grafana node dashboard:

  * why data from some nodes does not arrive?
  * set different default times (length and refres)
  * active job number
  * table of processes with highest load
    
* LAgent should be able to change frequency of measurements depending on the situation
  of the node
