
FROM python:3.8

RUN apt-get update -y && apt-get install -y ffmpeg

COPY ./backend/openssl.cnf  /etc/ssl/openssl.cnf

ENV PYTHONUNBUFFERED 1
COPY . /usr/src/app/
WORKDIR /usr/src/app

RUN pip3 install -r requirements.txt
