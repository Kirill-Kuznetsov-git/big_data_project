#!/bin/bash

psql -U postgres -f ../sql/create_table.sql

echo "Table created successfully."

psql -U postgres -f ../sql/load_csv.sql
