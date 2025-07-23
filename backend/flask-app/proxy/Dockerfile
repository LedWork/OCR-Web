FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="chriskondracki"

ENV LISTEN_PORT=80
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
