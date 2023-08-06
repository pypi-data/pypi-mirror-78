#######################
FrUCToSA's Requirements
#######################


* [R01] Central management
* [R07] Basic agent for jobs (Slurm)
* [R08] Grafana dashboards

  1. ...for nodes
  2. ...for jobs
  3. ...for the full cluster

* [R09] Automatic generation of plots for HKHLR and loewemon
* [R10] ML analysis of collected data to classify jobs (PerA)
* [R11] Architecture's revamp I

  * heartbeat mechanism
  * agents send data directly to destination(s)

* [R12] PerA: agent to *cook* raw data I

  * compute global metrics for the full cluster

* [R13] Agent for jobs (Slurm) II

  * it can link data from slurm (jobs) to data from other agents (nodes)

* [R14] Improved sensors

  * docs: command line mechanism to get info about sensors
  * parameters: implement mechanism to pass params to sensors

* [R15] Documentation

  * sensors
  * configuration files
  * command line options
  * man page
  * etc

