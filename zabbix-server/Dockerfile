FROM zabbix/zabbix-server-pgsql:ubuntu-6.0-latest
LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ=Asia/Shanghai
ENV LANG en_US.utf8

USER root

RUN set -ex; \
    # sed -i 's|archive.ubuntu.com|mirrors.aliyun.com|g' /etc/apt/sources.list; \
    # sed -i 's|security.ubuntu.com|mirrors.aliyun.com|g' /etc/apt/sources.list; \
    apt-get update; \
    apt-get -y upgrade; \
    apt-get -y install tzdata; \
    ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime; \
    echo ${TZ} > /etc/timezone; \
    dpkg-reconfigure --frontend noninteractive tzdata; \
    apt-get -y install locales; \
    localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8; \
    apt-get -y install python3-pip; \
    apt-get -y autoremove; \
    apt-get -y clean; \
    pip3 install --upgrade requests loguru pyzabbix;
