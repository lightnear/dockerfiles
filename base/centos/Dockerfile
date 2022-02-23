FROM centos:7

LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ=Asia/Shanghai

RUN ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone \
    && yum update -y \
    && yum install -y rsync curl wget git \
    && yum clean all

CMD ["bash"]
