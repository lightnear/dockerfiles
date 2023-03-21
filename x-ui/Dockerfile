FROM debian:stable

LABEL maintainer="lightnear<lightnear@qq.com>"

ARG TARGETPLATFORM
ARG BUILDPLATFORM

ENV DEBIAN_FRONTEND noninteractive
ENV TZ=Asia/Shanghai
ENV LANG en_US.UTF-8

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
  apt-get -y install locales locales-all; \
  localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8; \
  apt-get -y install ca-certificates; \
  apt-get -y autoremove; \
  apt-get -y clean;

RUN set -ex; \
  apt-get update; \
  apt-get -y install wget curl tar;

ENV XUI_USER admin
ENV XUI_PASS admin
ENV XUI_PORT 54321

SHELL ["/bin/bash", "-c"]
WORKDIR /usr/local/
RUN  cd /usr/local/; \
  latest_version=$(curl -sL "https://api.github.com/repos/FranzKafkaYu/x-ui/releases/latest" | \
  awk '/tag_name/{print $4;exit}' FS='[""]'); \
  [[ ! -n "$latest_version" ]] && echo -e "检测 x-ui 版本失败，可能是超出 Github API 限制，请稍后再试，或手动指定 x-ui 版本安装" && exit 1; \
  echo -e "检测到 x-ui 最新版本：${latest_version}，开始安装"; \
  arch=amd64; \
  [[ "$TARGETPLATFORM" == "linux/arm64" ]] && arch=arm64; \
  url="https://github.com/FranzKafkaYu/x-ui/releases/download/${latest_version}/x-ui-linux-${arch}.tar.gz"; \
  wget -N --no-check-certificate -O /usr/local/x-ui-linux-${arch}.tar.gz ${url}; \
  [[ -e /usr/local/x-ui/ ]] && rm -rf /usr/local/x-ui/; \
  tar zxvf x-ui-linux-${arch}.tar.gz; \
  rm -rf x-ui-linux-${arch}.tar.gz; \
  cd x-ui; \
  chmod +x x-ui bin/xray-linux-${arch}; \
  wget --no-check-certificate -O /usr/bin/x-ui https://raw.githubusercontent.com/FranzKafkaYu/x-ui/main/x-ui.sh; \
  chmod +x /usr/local/x-ui/x-ui.sh; \
  chmod +x /usr/bin/x-ui;

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

VOLUME /etc/x-ui
WORKDIR /usr/local/x-ui/
ENTRYPOINT ["docker-entrypoint.sh"]
CMD [ "/usr/local/x-ui/x-ui" ]
