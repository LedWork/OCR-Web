#!/bin/sh
set -e

uwsgi --http :8000 --workers 2 --master --enable-threads --module app:app
