#!/bin/bash

/usr/local/bin/wait_for_it.sh $POSTGRES_HOST:$POSTGRES_PORT -t 60

python manage.py migrate

gunicorn trazip.wsgi -b 0.0.0.0:80 --workers 3 --log-level DEBUG
