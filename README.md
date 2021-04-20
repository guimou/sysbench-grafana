# Sysbench with Grafana dashboard

## Installation

* Deploy a MariaDB database in you project using OpenShift Dev view
* Connect to the DB (terminal view) and initiate it with commands in the SQL.txt file
* Deploy the Grafana operator, along with the DataSource and Dashboard files
* Create the Sysbench Job with `sysbench-rwx-rwrite-4k-log.yaml`

## Sysbench custom Job

* To modify the sysbench part, you can create a custom image from [this repo](https://github.com/red-hat-storage/ocs-training/tree/master/training/modules/ocs4perf/attachments). Modify files as needed and recreate container image.
* To modify the logging part, you can modify the data-write Python script and rebuild the container image
* Update the yaml job to use the right images!