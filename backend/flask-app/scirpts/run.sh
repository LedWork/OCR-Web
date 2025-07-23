#!/bin/sh
set -e

uwsgi --http :80 --workers 2 --master --enable-threads --module app:app
