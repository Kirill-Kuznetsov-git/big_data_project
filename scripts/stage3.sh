#!/bin/bash

rm -rf output/q1*
rm -rf output/q2*
rm -rf output/q3*
rm -rf output/q4*
rm -rf output/q5*
rm -rf output/q6*
rm -rf output/q7*
rm -rf output/evaluation*
rm -rf output/pipeline_output*
rm -rf output/lr*
rm -rf output/rf*

# python3 scripts/EDA.py
spark-submit --jars /usr/hdp/current/hive-client/lib/hive-metastore-1.2.1000.2.6.5.0-292.jar,/usr/hdp/current/hive-client/lib/hive-exec-1.2.1000.2.6.5.0-292.jar --packages org.apache.spark:spark-avro_2.12:3.0.3 scripts/EDA.py

# python3 scripts/PDA.py
spark-submit --jars /usr/hdp/current/hive-client/lib/hive-metastore-1.2.1000.2.6.5.0-292.jar,/usr/hdp/current/hive-client/lib/hive-exec-1.2.1000.2.6.5.0-292.jar --packages org.apache.spark:spark-avro_2.12:3.0.3 scripts/PDA.py

# merge csv files into one

echo "" > output/q1.csv
cat output/q1/* >> output/q1.csv

echo "" > output/q2.csv
cat output/q2/* >> output/q2.csv

echo "" > output/q3.csv
cat output/q3/* >> output/q3.csv

echo "" > output/q4.csv
cat output/q4/* >> output/q4.csv

echo "" > output/q5.csv
cat output/q5/* >> output/q5.csv

echo "" > output/q6.csv
cat output/q6/* >> output/q6.csv

echo "" > output/q7.csv
cat output/q7/* >> output/q7.csv

echo "" > output/evaluation.csv
cat output/evaluation/* >> output/evaluation.csv

echo "" > output/pipeline_output.csv
cat output/pipeline_output/* >> output/pipeline_output.csv

echo "" > output/lr.csv
cat output/lr/* >> output/lr.csv

echo "" > output/rf.csv
cat output/rf/* >> output/rf.csv