DROP DATABASE IF EXISTS projectdb;

CREATE DATABASE projectdb;
USE projectdb;

SET mapreduce.map.output.compress = true;
SET mapreduce.map.output.compress.codec = org.apache.hadoop.io.compress.SnappyCodec;

DROP TABLE trips;

CREATE EXTERNAL TABLE trips STORED AS AVRO LOCATION '/project/trips' TBLPROPERTIES ('avro.schema.url'='/project/trips.avsc');
