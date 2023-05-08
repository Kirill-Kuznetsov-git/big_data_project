#!/bin/bash

wget https://jdbc.postgresql.org/download/postgresql-42.6.0.jar --no-check-certificate

cp  postgresql-42.6.0.jar /usr/hdp/current/sqoop-client/lib/

psql -U postgres -f sql/create_database.sql

echo "Database created successfully."

psql -d project -U postgres -f sql/create_table.sql

echo "Table created successfully."

psql -d project -U postgres -f sql/load_csv.sql

echo "Data from csv loaded successfully."

sqoop import-all-tables -Dmapreduce.job.user.classpath.first=true \
 -Dorg.apache.sqoop.splitter.allow_text_splitter=true \
 --connect jdbc:postgresql://localhost/project \
 --username postgres --warehouse-dir /project \
 --as-avrodatafile --compression-codec=snappy \
 --outdir /project --m 1

echo "Data from csv PG to HDFS imported successfully."
