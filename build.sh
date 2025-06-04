#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python passlock/manage.py collectstatic --no-input

python passlock/manage.py migrate