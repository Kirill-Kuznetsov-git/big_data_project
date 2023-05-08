#!/bin/bash

hdfs dfs -put /project/avsc/trips.avsc /project/trips.avsc

echo "Avsc file imported from local machine to hdfs successfully."

hive -f sql/db.hql
