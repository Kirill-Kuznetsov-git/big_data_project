#!/bin/bash

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1xlhxseaFSlpI6MTfa7ks91CG3RKrzmUQ' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1xlhxseaFSlpI6MTfa7ks91CG3RKrzmUQ" -O data/trips.tsv && rm -rf /tmp/cookies.txt

wget https://jdbc.postgresql.org/download/postgresql-42.6.0.jar --no-check-certificate

cp  postgresql-42.6.0.jar /usr/hdp/current/sqoop-client/lib/

psql -U postgres -f sql/create_database.sql

echo "Database created successfully."

psql -d project -U postgres -f sql/create_table.sql

echo "Table created successfully."

psql -d project -U postgres -f sql/load_csv.sql

echo "Data from csv loaded successfully."

hdfs dfs -rm -r /project
rm /project/trips.avsc

sqoop import-all-tables -Dmapreduce.job.user.classpath.first=true \
 -Dorg.apache.sqoop.splitter.allow_text_splitter=true \
 --connect jdbc:postgresql://localhost/project \
 --username postgres --warehouse-dir /project \
 --as-avrodatafile --compression-codec=snappy \
 --outdir /project --m 1

echo "Data from csv PG to HDFS imported successfully."

hdfs dfs -put /project/trips.avsc /project/trips.avsc

echo "Avsc file imported from local machine to hdfs successfully."
