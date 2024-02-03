FROM python:3

LABEL maintainer="lightnear<lightnear@qq.com>"

ENV TZ=Asia/Shanghai
ENV LANG en_US.utf8

COPY requirements.txt .
RUN pip install --upgrade --no-cache pip setuptools wheel; \
  pip install --no-cache -r requirements.txt; \
  pip cache purge;

WORKDIR /app

VOLUME [ "/config" ]

CMD [ "python", "-u", "main.py" ]

