FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="chriskondracki"

USER root

RUN apk add --no-cache \
    certbot \
    py3-pip \
    curl \
    bash \
    libffi \
    ca-certificates \
    openssl && \
    python3 -m venv /opt/certbot && \
    /opt/certbot/bin/pip install --no-cache-dir certbot-nginx && \
    ln -sf /opt/certbot/bin/certbot /usr/local/bin/certbot


COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

ENV LISTEN_PORT=8000
ENV APP_HOST=app
ENV APP_PORT=9000

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME /vol/static

USER nginx

CMD ["/run.sh"]
