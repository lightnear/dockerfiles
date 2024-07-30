FROM python:3

LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ Asia/Shanghai
ENV LANG en_US.utf8

RUN pip install --upgrade pip setuptools; \
  pip install --no-cache-dir wheel; \
  pip install --no-cache-dir loguru requests fake_useragent schedule pyyaml;

WORKDIR /app

VOLUME [ "/config" ]

CMD [ "python", "-u", "main.py" ]

