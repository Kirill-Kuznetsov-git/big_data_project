#!/bin/bash

rm -rf output/evaluation*
rm -rf output/lr*
rm -rf output/rf*
# rm -rf output/gbt*

rm -rf models/*

# python scripts/pda_file.py
spark-submit --jars /usr/hdp/current/hive-client/lib/hive-metastore-1.2.1000.2.6.5.0-292.jar,/usr/hdp/current/hive-client/lib/hive-exec-1.2.1000.2.6.5.0-292.jar --packages org.apache.spark:spark-avro_2.12:3.0.3 scripts/pda_file.py

# merge csv files into one

echo "trip_time_sec,prediction" > output/lr.csv
cat output/lr/* >> output/lr.csv

echo "trip_time_sec,prediction" > output/rf.csv
cat output/rf/* >> output/rf.csv

# echo "trip_time_sec,prediction" > output/gbt.csv
# cat output/gbt/* >> output/gbt.csv

