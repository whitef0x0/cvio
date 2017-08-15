#!/bin/bash

# Create database and apply migrations
echo "Create Database"
python manage.py create_db

# Apply Migrations
echo "Apply migrations"
python manage.py db upgrade
python manage.py db migrate

# Start server
echo "Starting server"
/usr/bin/supervisord