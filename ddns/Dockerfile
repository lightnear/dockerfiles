FROM python:3

LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ=Asia/Shanghai
ENV LANG en_US.utf8

RUN pip install --upgrade pip setuptools; \
  pip install --no-cache-dir wheel; \
  pip install --no-cache-dir requests schedule; \
  pip install --no-cache-dir pyyaml;

COPY ddns/ /app/

WORKDIR /app

VOLUME [ "/etc/ddns/config.json" ]

CMD [ "python", "-u", "main.py" ]

