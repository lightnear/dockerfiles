FROM alpine:latest

LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ=Asia/Shanghai

RUN apk add --no-cache tzdata; \
    cp /usr/share/zoneinfo/${TZ} /etc/localtime; \
    echo ${TZ} > /etc/timezone; \
    apk del tzdata; \
    apk add --no-cache bash wget curl;

RUN cd /root; \
    FRP_VERSION=$(curl -sX GET "https://api.github.com/repos/fatedier/frp/releases/latest" | awk '/tag_name/{print $4;exit}' FS='[""]'); \
    FRP_VERSION=$(echo $FRP_VERSION | tr -d 'v'); \
    FRP_VERSION=${FRP_VERSION:-1.0.0}; \
    wget --no-check-certificate -c https://github.com/fatedier/frp/releases/download/v${FRP_VERSION}/frp_${FRP_VERSION}_linux_amd64.tar.gz; \
    tar zxvf frp_${FRP_VERSION}_linux_amd64.tar.gz;  \
    cd frp_${FRP_VERSION}_linux_amd64/; \
    cp frps /usr/bin/; \
    cp frpc /usr/bin/; \
    mkdir -p /etc/frp; \
    cp frps.ini /etc/frp; \
    cp frpc.ini /etc/frp; \
    cd /root; \
    rm frp_${FRP_VERSION}_linux_amd64.tar.gz; \
    rm -rf frp_${FRP_VERSION}_linux_amd64/;

VOLUME /etc/frp

CMD ["bash"]
