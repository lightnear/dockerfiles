FROM zabbix/zabbix-server-pgsql:alpine-6.0-latest
LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ=Asia/Shanghai
ENV LANG en_US.utf8

USER root

RUN set -ex; \
    # sed -i 's|archive.ubuntu.com|mirrors.aliyun.com|g' /etc/apt/sources.list; \
    # sed -i 's|security.ubuntu.com|mirrors.aliyun.com|g' /etc/apt/sources.list; \
    apk add --no-cache bash tzdata ca-certificates; \
    cp /usr/share/zoneinfo/${TZ} /etc/localtime; \
    echo ${TZ} > /etc/timezone; \
    apk add --no-cache python3 py3-pip


COPY requirements.txt .
RUN pip install --upgrade --no-cache pip setuptools wheel; \
  pip install --no-cache -r requirements.txt; \
  pip cache purge;
