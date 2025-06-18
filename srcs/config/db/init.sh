#!/bin/bash

echo "Starting database migration..."
python srcs/manage.py migrate

echo "Starting development server..."
python srcs/manage.py runserver 0.0.0.0:8000 