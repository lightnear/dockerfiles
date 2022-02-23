FROM python:3

LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ=Asia/Shanghai
ENV LANG en_US.utf8

RUN pip install --no-cache-dir aliyun-python-sdk-core-v3 aliyun-python-sdk-alidns requests schedule \
    -i https://mirrors.aliyun.com/pypi/simple

COPY ddns/* .

VOLUME [ "/etc/ddns/config.json" ]

CMD [ "python", "-u", "main.py" ]
