FROM python:3

LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ=Asia/Shanghai
ENV LANG en_US.utf8

RUN pip install --no-cache-dir requests schedule; \
  pip install --no-cache-dir alibabacloud_tea_openapi; \
  pip install --no-cache-dir alibabacloud_alidns20150109==2.0.2;
  # pip install --no-cache-dir tencentcloud-sdk-python;

COPY ddns/* .

VOLUME [ "/etc/ddns/config.json" ]

CMD [ "python", "-u", "main.py" ]

