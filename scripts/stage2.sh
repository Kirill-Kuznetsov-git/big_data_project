#!/bin/bash

hive -f sql/db.hql


rm -rf output/trips_preprocessed*
rm -rf output/q1*
rm -rf output/q2*
rm -rf output/q3*
rm -rf output/q4*
rm -rf output/q5*
rm -rf output/q6*
rm -rf output/q7*


# python scripts/EDA.py
spark-submit --jars /usr/hdp/current/hive-client/lib/hive-metastore-1.2.1000.2.6.5.0-292.jar,/usr/hdp/current/hive-client/lib/hive-exec-1.2.1000.2.6.5.0-292.jar --packages org.apache.spark:spark-avro_2.12:3.0.3 scripts/EDA.py


# merge csv files into one

echo "trip_id,call_type,origin_call,origin_stand,taxi_id,timestamp,day_type,missing_data,polyline,year,month,day,hour,day_of_week,polyline_length,trip_time_sec" > output/trips_preprocessed.csv
cat output/trips_preprocessed/* >> output/trips_preprocessed.csv

echo "trip_id,call_type,origin_call,origin_stand,taxi_id,timestamp,day_type,missing_data,polyline,year,month,day,hour,day_of_week,polyline_length,trip_time_sec" > output/q1.csv
cat output/q1/* >> output/q1.csv

echo "day_of_week,avg_trip_time" > output/q2.csv
cat output/q2/* >> output/q2.csv

echo "hour,avg_trip_time" > output/q3.csv
cat output/q3/* >> output/q3.csv

echo "call_type,avg_trip_time" > output/q4.csv
cat output/q4/* >> output/q4.csv

echo "call_type,count_trip_time" > output/q5.csv
cat output/q5/* >> output/q5.csv

echo "avg_trip_time,max_trip_time,min_trip_time" > output/q6.csv
cat output/q6/* >> output/q6.csv

echo "day_type,count" > output/q7.csv
cat output/q7/* >> output/q7.csv
