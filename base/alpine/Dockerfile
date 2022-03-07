FROM alpine:latest

LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ=Asia/Shanghai

RUN apk add --no-cache tzdata; \
    cp /usr/share/zoneinfo/${TZ} /etc/localtime; \
    echo ${TZ} > /etc/timezone; \
    apk del tzdata; \
    apk add --no-cache bash wget curl rsync openssh-client-default git;

CMD ["bash"]
