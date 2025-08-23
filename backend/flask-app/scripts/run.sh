#!/bin/sh
set -e

gunicorn --workers 2 --bind 0.0.0.0:5000 --threads 4 --max-requests 1000 --max-requests-jitter 100 --timeout 120 --keep-alive 5 --max-requests-inflight 1000 --max-requests-per-child 1000 --worker-connections 1000 --worker-tmp-dir /dev/shm --preload app:app
