FROM zabbix/zabbix-server-mysql:ubuntu-5.0-latest
LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ=Asia/Shanghai
ENV LANG en_US.utf8

USER root

RUN sed -i 's|archive.ubuntu.com|mirrors.aliyun.com|g' /etc/apt/sources.list \
    && sed -i 's|security.ubuntu.com|mirrors.aliyun.com|g' /etc/apt/sources.list \
    && DEBIAN_FRONTEND=noninteractive apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get -y upgrade \
    && DEBIAN_FRONTEND=noninteractive apt-get -y autoremove \
    && DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata \
    && ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && DEBIAN_FRONTEND=noninteractive apt-get -y install locales \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip \
    && DEBIAN_FRONTEND=noninteractive apt-get -y autoremove \
    && DEBIAN_FRONTEND=noninteractive apt-get -y clean \
    && pip3 install requests \
    && pip3 install --upgrade requests
