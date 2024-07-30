FROM ubuntu:22.04

LABEL maintainer="lightnear<lightnear@qq.com>"

ENV DEBIAN_FRONTEND noninteractive
ENV TZ Asia/Shanghai
ENV LANG en_US.UTF-8

RUN set -ex; \
    # sed -i 's|archive.ubuntu.com|mirrors.aliyun.com|g' /etc/apt/sources.list; \
    # sed -i 's|security.ubuntu.com|mirrors.aliyun.com|g' /etc/apt/sources.list; \
    apt-get update; \
    apt-get -y upgrade; \
    apt-get -y install tzdata; \
    ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime; \
    echo ${TZ} > /etc/timezone; \
    dpkg-reconfigure --frontend noninteractive tzdata; \
    apt-get -y install locales locales-all; \
    localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8; \
    apt-get -y install openssh-client rsync curl wget sudo git bzip2 bc snmp snmp-mibs-downloader ipmitool iperf3 ca-certificates; \
    apt-get -y autoremove; \
    apt-get -y clean;

CMD ["bash"]
