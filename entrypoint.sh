#!/bin/bash

echo "Apply data migrations"
python manage.py migrate



exec "$@"