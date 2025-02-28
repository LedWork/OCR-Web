FROM python:3.10-alpine3.13
LABEL maintainer="chriskondracki"

ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
COPY ./scirpts /scripts
WORKDIR /app
EXPOSE 5000

RUN apk add --no-cache musl-dev gcc python3-dev libffi-dev pcre-dev linux-headers && \
    python -m venv /py && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        flaskuser && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/uploads && \
    chown -R flaskuser:flaskuser /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts


ENV PATH="/scripts:/py/bin:$PATH"


USER flaskuser

CMD ["run.sh"]