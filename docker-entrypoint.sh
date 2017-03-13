#!/bin/bash

/usr/local/bin/wait_for_it.sh $POSTGRES_HOST:$POSTGRES_PORT -t 60

echo 'Migrating database changes.'
python manage.py migrate

echo 'Creating super user.'
echo "from django.contrib.auth.models import User; \
User.objects.create_superuser('admin', 'admin@admin.com', \
'${SUPERUSER_PASSWORD}')" | python manage.py shell 2> /dev/null

echo 'Generating data to database.'
python manage.py seed

gunicorn trazip.wsgi -b 0.0.0.0:80 --workers 3 --log-level DEBUG
