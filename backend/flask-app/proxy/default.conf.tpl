server {
    listen ${LISTEN_PORT};

    server_tokens off;
    add_header X-Content-Type-Options nosniff;

    location ~ /(BitKeeper|\.git|\.hg|\.svn|\.env|\.config|\.key|\.log|\.sql|\.sh|\.bzr|._darcs) {
        deny all;
        return 403;
    }

    location /static {
        alias /vol/static;
    }

    location / {
        proxy_pass              http://${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
    }
}