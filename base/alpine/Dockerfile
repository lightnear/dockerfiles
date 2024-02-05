FROM alpine:latest

LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ=Asia/Shanghai
ENV LANG en_US.utf8

RUN set -ex; \
    apk add --no-cache bash tzdata ca-certificates wget curl rsync openssh-client-default git; \
    cp /usr/share/zoneinfo/${TZ} /etc/localtime; \
    echo ${TZ} > /etc/timezone;

CMD ["bash"]
