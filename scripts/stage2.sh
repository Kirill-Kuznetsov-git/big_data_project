#!/bin/bash

hdfs dfs -put /project/avsc/*.avsc /project/avsc

echo "Avsc file imported from local machine to hdfs successfully."

hive -f ../sql/db.hql
