#!/bin/bash
set -e

# Run database migrations
# NOTE: This is not an ideal solution since this database
# migration step will run every time the container is executed.
python manage.py migrate

# Load initial data
# NOTE: This is also not ideal because not every time we
# will want the sample data to be present.
python manage.py loaddata initial.json sample.json

exec "$@"
