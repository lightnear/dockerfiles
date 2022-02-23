FROM ubuntu:20.04

LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ=Asia/Shanghai
ENV LANG en_US.utf8

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
    && DEBIAN_FRONTEND=noninteractive apt-get -y install openssh-client rsync curl wget sudo git \
    && DEBIAN_FRONTEND=noninteractive apt-get -y install bzip2 bc snmp snmp-mibs-downloader ipmitool iperf3 \
    && DEBIAN_FRONTEND=noninteractive apt-get -y autoremove \
    && DEBIAN_FRONTEND=noninteractive apt-get -y clean

CMD ["bash"]
