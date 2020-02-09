#!/bin/bash
set -e

# Run database migrations
# NOTE: This is not an ideal solution since this database
# migration step will run every time the container is executed.
python manage.py migrate

exec "$@"
