FROM python:3

LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ=Asia/Shanghai
ENV LANG en_US.utf8

RUN pip install --upgrade pip setuptools; \
  pip install --no-cache-dir wheel; \
  pip install --no-cache-dir requests requests-cache schedule; \
  pip install --no-cache-dir pyyaml lxml cn2an;

COPY app/ /app/

WORKDIR /app

VOLUME [ "/config" ]

CMD [ "python", "-u", "main.py" ]

