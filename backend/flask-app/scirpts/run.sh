#!/bin/sh
set -e

gunicorn --workers 2 --bind 0.0.0.0:5000 --threads 4 app:app
