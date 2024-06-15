FROM zabbix/zabbix-server-pgsql:alpine-7.0-latest
LABEL maintainer="lightnear<lightnear@qq.com>"

USER root

ENV TZ=Asia/Shanghai
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN set -ex; \
    apk add --update --no-cache bash tzdata locales ca-certificates; \
    cp /usr/share/zoneinfo/${TZ} /etc/localtime; \
    echo ${TZ} > /etc/timezone; \
    localedef -c -f UTF-8 -i en_US en_US.UTF-8;

RUN apk del tzdata;

RUN set -ex; \
    apk add --update --no-cache python3; \
    ln -sf python3 /usr/bin/python; \
    python3 -m ensurepip; \
    pip3 install --no-cache --upgrade pip setuptools;

COPY requirements.txt .
RUN pip3 install --upgrade --no-cache pip setuptools wheel; \
  pip3 install --no-cache -r requirements.txt; \
  pip3 cache purge;
