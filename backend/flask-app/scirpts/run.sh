#!/bin/sh
set -e

uwsgi --http :9000 --workers 4 --master --enable-threads --module app:app



