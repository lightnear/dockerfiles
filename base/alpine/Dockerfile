FROM alpine:latest

LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ=Asia/Shanghai
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN set -ex; \
    apk add --no-cache bash tzdata locales; \
    cp /usr/share/zoneinfo/${TZ} /etc/localtime; \
    echo ${TZ} > /etc/timezone; \
    localedef -c -f UTF-8 -i en_US en_US.UTF-8;

RUN apk del tzdata;

RUN apk add --no-cache ca-certificates wget curl rsync openssh-client-default git

CMD ["bash"]
