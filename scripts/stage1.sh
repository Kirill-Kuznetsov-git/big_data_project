#!/bin/bash

psql -d project -U postgres -f ../sql/create_table.sql

echo "Table created successfully."

psql -d project -U postgres -f ../sql/load_csv.sql
