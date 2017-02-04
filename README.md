# Trazip

## What is Trazip
Trazip is trying to simplify the way to plan a trip. Get rid of comparing hotels price, deciding which view you'd like to visit or fly tickets. Just tell us the budget and time, we will handle rest part of it.

## To developers
In order to run the website in standalone mode for development purpose, please do following steps:

0. cd trazip home dir
1. `python manage.py makemigrations`
2. `python manage.py migrate`
3. `export DJANGO_SETTINGS_MODULE=trazip.settings`
4. `export PYTHONPATH=path/to/trazip`
5. `python scripts/temp_spider.py`
6. `python manage.py runserver`