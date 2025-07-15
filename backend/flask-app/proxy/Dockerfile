FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="chriskondracki"

USER root

RUN apk add --no-cache \
        certbot \
        py3-pip \
        curl \
        bash \
        libffi \
        libssl1.1 \
        ca-certificates \
        openssl && \
    pip install --no-cache-dir certbot-nginx

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
