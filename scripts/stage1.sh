#!/bin/bash

# Draft: Create the table
# TODO: Note: Do not forget, that the file .sql should not return errors when you run it for the second time,
#       so you should clear/drop the objects before creating new database objects.

# SQL statement to create the table
SQL_STATEMENT="
CREATE TABLE IF NOT EXISTS trips (
    trip_id VARCHAR(120) PRIMARY KEY,
    call_type VARCHAR(10) NOT NULL,
    origin_call INTEGER NULL,
    origin_stand INTEGER NULL,
    taxi_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    day_type VARCHAR(10) NOT NULL,
    missing_data BOOLEAN NOT NULL,
    polyline TEXT NOT NULL
);
"

psql -U postgres -c "$SQL_STATEMENT" || exit 1

echo "Table created successfully."

# TODO: Load data from csv files.
psql -U postgres -f ../sql/load_csv.sql
