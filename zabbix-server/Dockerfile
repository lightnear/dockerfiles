FROM zabbix/zabbix-server-pgsql:alpine-7.0-latest
LABEL maintainer="lightnear<lightnear@qq.com>"

USER root

ENV TZ=Asia/Shanghai
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN set -ex; \
    apk add --no-cache bash tzdata musl-locales; \
    cp /usr/share/zoneinfo/${TZ} /etc/localtime; \
    echo ${TZ} > /etc/timezone; \
    echo "export LC_ALL=${LC_ALL}" > /etc/profile.d/locale.sh; \
    echo "export LANG=${LANG}" >> /etc/profile.d/locale.sh; \
    chmod +x /etc/profile.d/locale.sh; \
    /etc/profile.d/locale.sh;

RUN apk del tzdata;

RUN set -ex; \
    apk add --update --no-cache python3 py3-pip; \
    ln -sf python3 /usr/bin/python; \
    # python3 -m ensurepip; \
    pip3 install --no-cache --upgrade --break-system-packages pip setuptools wheel;

COPY requirements.txt .
RUN pip3 install --no-cache --break-system-packages -r requirements.txt; \
    pip3 cache purge;
