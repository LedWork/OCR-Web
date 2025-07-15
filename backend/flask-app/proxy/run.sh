#!/bin/sh

set -e
envsubst '$${LISTEN_PORT},$${APP_PORT},$${APP_HOST}' < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

CERT_DIR="/etc/letsencrypt/live/${APP_HOST}"
if [ ! -d "$CERT_DIR" ]; then
  echo "=> First‑time certificate request for ${APP_HOST}"
  certbot certonly --standalone \
    --non‑interactive \
    --agree-tos \
    --email "$CERT_EMAIL" \
    -d "$APP_HOST"
fi

crond

nginx -g 'daemon off;'