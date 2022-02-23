FROM debian:11

LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ=Asia/Shanghai
ENV LANG en_US.utf8

RUN echo 'deb http://mirrors.aliyun.com/debian/ bullseye main non-free contrib' > /etc/apt/sources.list \
    && echo 'deb http://mirrors.aliyun.com/debian-security/ bullseye-security main' >> /etc/apt/sources.list \
    && echo 'deb http://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib' >> /etc/apt/sources.list \
    && echo 'deb http://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib' >> /etc/apt/sources.list \
    && DEBIAN_FRONTEND=noninteractive apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get -y upgrade \
    && DEBIAN_FRONTEND=noninteractive apt-get -y autoremove \
    && DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata \
    && ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && DEBIAN_FRONTEND=noninteractive apt-get -y install locales \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 \
    && DEBIAN_FRONTEND=noninteractive apt-get -y install git rsync awscli stunnel4 socat \
    && DEBIAN_FRONTEND=noninteractive apt-get -y autoremove \
    && DEBIAN_FRONTEND=noninteractive apt-get -y clean

RUN git clone https://ftp-master.debian.org/git/archvsync.git/ /ftpsync/

WORKDIR /ftpsync/
ENV PATH /ftpsync/bin:${PATH}

CMD ["bash"]
