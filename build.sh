#!/usr/bin/env bash
set -o errexit

cd passlock
pip install -r requirements.txt

python passlock/passlock/manage.py collectstatic --no-input

python passlock/passlock/manage.py migrate