FROM rockylinux:9

LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ=Asia/Shanghai

RUN set -ex; \
    ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime; \
    echo ${TZ} > /etc/timezone; \
    dnf -y update; \
    dnf -y install --allowerasing rsync curl wget git; \
    dnf clean all;

CMD ["bash"]
