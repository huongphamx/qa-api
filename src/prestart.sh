#! /usr/bin/env bash

# check for db connection
python /app/app/backend_pre_start.py

# run migration
echo "Running migration"
alembic upgrade head
echo "Finished migration"

# Let the DB start
python /app/app/initial_data.py
