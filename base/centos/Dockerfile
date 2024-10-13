FROM centos:7

LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ=Asia/Shanghai

RUN set -ex; \
    ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime; \
    echo ${TZ} > /etc/timezone; \
    yum -y update; \
    yum -y install rsync curl wget git; \
    yum clean all;

CMD ["bash"]
