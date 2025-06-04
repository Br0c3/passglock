#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python passlock/passlock/manage.py collectstatic --no-input

python passlock/passlock/manage.py migrate