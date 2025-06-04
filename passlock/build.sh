#!/usr/bin/env bash
set -o errexit

cd passlock
pip install -r requirements.txt

python manage.py collectstatic --no-input

python passlock/manage.py migrate