FROM python:3

LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ Asia/Shanghai
ENV LANG en_US.utf8

RUN pip install --upgrade pip setuptools; \
  pip install --no-cache-dir wheel; \
  pip install --no-cache-dir loguru requests requests-cache fake_useragent; \
  pip install --no-cache-dir schedule pyyaml lxml Brotli cn2an aiohttp bs4; \
  pip install --no-cache-dir pymysql sqlalchemy pytest; \
  pip install --no-cache-dir pysocks qbittorrent-api dacite;

WORKDIR /app

VOLUME [ "/config" ]

CMD [ "python", "-u", "main.py" ]

