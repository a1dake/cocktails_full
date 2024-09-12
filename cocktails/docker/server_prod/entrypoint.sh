#!/bin/sh

python manage.py migrate
python manage.py collectstatic --no-input
gunicorn main_core.wsgi:application -b 0.0.0.0:8000 --workers 9
