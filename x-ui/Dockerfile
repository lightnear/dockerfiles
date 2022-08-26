FROM debian:stable

LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ=Asia/Shanghai
ENV LANG en_US.utf8

# Do not use https, because ca-certificates is not installed and certificate verification failed error would accour
RUN set -ex; \
    # echo 'deb http://mirrors.aliyun.com/debian/ bullseye main non-free contrib' > /etc/apt/sources.list; \
    # echo 'deb http://mirrors.aliyun.com/debian-security/ bullseye-security main' >> /etc/apt/sources.list; \
    # echo 'deb http://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib' >> /etc/apt/sources.list; \
    # echo 'deb http://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib' >> /etc/apt/sources.list; \
    apt-get update; \
    apt-get -y upgrade; \
    apt-get -y install tzdata; \
    ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime; \
    echo ${TZ} > /etc/timezone; \
    dpkg-reconfigure --frontend noninteractive tzdata; \
    apt-get -y install locales; \
    localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8; \
    apt-get -y autoremove; \
    apt-get -y clean;

RUN set -ex; \
  apt-get -y install wget curl;

VOLUME /app/x-ui
VOLUME /etc/x-ui

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["/app/x-ui/x-ui"]
