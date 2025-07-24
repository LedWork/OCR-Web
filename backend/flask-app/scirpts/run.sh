#!/bin/sh
set -e

uwsgi --http :5000 --workers 2 --master --enable-threads --module app:app
