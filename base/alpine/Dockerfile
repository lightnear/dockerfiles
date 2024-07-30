FROM alpine:latest

LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ Asia/Shanghai
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN set -ex; \
    apk add --no-cache bash tzdata musl-locales; \
    cp /usr/share/zoneinfo/${TZ} /etc/localtime; \
    echo ${TZ} > /etc/timezone; \
    echo "export LC_ALL=${LC_ALL}" > /etc/profile.d/locale.sh; \
    echo "export LANG=${LANG}" >> /etc/profile.d/locale.sh; \
    chmod +x /etc/profile.d/locale.sh; \
    /etc/profile.d/locale.sh;

RUN apk del tzdata;

RUN apk add --no-cache ca-certificates wget curl rsync openssh-client-default git

CMD ["bash"]
