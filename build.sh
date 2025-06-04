#!/usr/bin/env bash
set -o errexit

pip install -r requirement.txt

python passlock/passlock/manage.py collectstatic --no-input

python passlock/passlock/manage.py migrate