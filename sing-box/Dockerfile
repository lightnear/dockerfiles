FROM golang:1.19-alpine AS builder
LABEL maintainer="lightnear <lightnear2012@gmail.com>"

ENV TZ=Asia/Shanghai
WORKDIR /go/src/github.com/sagernet/sing-box
ARG GOPROXY=""
ENV GOPROXY ${GOPROXY}
ENV CGO_ENABLED=1

RUN set -ex; \
    apk add --no-cache git build-base curl; \
    cd /go/src/github.com/sagernet; \
    LATEST_VERSION=$(curl -sX GET "https://api.github.com/repos/SagerNet/sing-box/releases/latest" | \
      awk '/tag_name/{print $4;exit}' FS='[""]'); \
    LATEST_VERSION=${LATEST_VERSION:-1.0.6}; \
    LATEST_VERSION=v1.1-beta15; \
    git clone -b $LATEST_VERSION https://github.com/SagerNet/sing-box.git; \
    cd sing-box; \
    export COMMIT=$(git rev-parse --short HEAD); \
    go build -v -trimpath -tags \
      with_quic,with_grpc,with_wireguard,with_shadowsocksr,with_ech,with_utls,with_acme,with_clash_api,with_gvisor,with_lwip \
      -o /go/bin/sing-box \
      -ldflags "-s -w -buildid=" \
      ./cmd/sing-box

FROM alpine AS dist
LABEL maintainer="lightnear <lightnear2012@gmail.com>"
ENV TZ=Asia/Shanghai
# RUN [ ! -e /etc/nsswitch.conf ] && echo 'hosts: files dns' > /etc/nsswitch.conf
RUN set -ex; \
    apk upgrade; \
    apk add --no-cache bash tzdata ca-certificates; \
    ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime;
COPY --from=builder /go/bin/sing-box /usr/local/bin/sing-box
ENTRYPOINT ["sing-box"]
