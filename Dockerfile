FROM python:3.9-alpine

LABEL Maintainer="Muhammad Fajar Febriano <fajarfebriano@gmail.com>" \
      Description="Python 3.8 Alpine Linux can run with Flask framework"

ENV PYTHONUNBUFFERED 1

ARG TZ='Asia/Jakarta'
ENV DEFAULT_TZ ${TZ}
RUN \
    apk update && \
    apk add -U tzdata && \
    cp /usr/share/zoneinfo/${TZ} /etc/localtime && \
    apk del tzdata && \
    apk add postgresql-libs && \
    apk add gcc musl-dev libc-dev linux-headers postgresql-dev && \
    rm -rf \
    /var/cache/apk/*

# ==== init location path project ====
RUN  mkdir /app
COPY . /app/
WORKDIR /app/

RUN pip install -r requirements.txt

EXPOSE 8000


