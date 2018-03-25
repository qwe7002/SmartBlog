FROM alpine:latest

ENV LANG C.UTF-8

WORKDIR /home/silverblog/

RUN apk add --no-cache python3 git nano vim bash uwsgi uwsgi-python3 newt ca-certificates \
&& python3 -m pip install -U pip \
&& update-ca-certificates \
&& apk add --no-cache --virtual .build-deps musl-dev gcc python3-dev \
&& pip3 install flask hoedown xpinyin pyrss2gen gitpython watchdog requests \
&& apk del --purge .build-deps