
FROM python:3.8

RUN apt-get update -y && apt-get install -y ffmpeg transmission-daemon build-essential pkg-config git zlib1g-dev

COPY ./backend/openssl.cnf  /etc/ssl/openssl.cnf

RUN git clone --depth=1 --branch v1.0.1 https://github.com/gpac/gpac gpac_public && cd gpac_public && ./configure --static-mp4box && make && make install

RUN apt-get remove -y build-essential pkg-config git

ENV PYTHONUNBUFFERED 1
#COPY ./backend/ /usr/src/app/
#WORKDIR /usr/src/app
ADD ./backend/requirements.txt /srv/requirements.txt
RUN pip install -r /srv/requirements.txt

WORKDIR /usr/src/app

