
FROM jrottenberg/ffmpeg:4.4-ubuntu2004
ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y && apt-get install -y transmission-daemon build-essential pkg-config git zlib1g-dev python3-pip

COPY ./backend/openssl.cnf  /etc/ssl/openssl.cnf

RUN git clone --depth=1 --branch v1.0.1 https://github.com/gpac/gpac gpac_public && cd gpac_public && ./configure --static-mp4box && make && make install

RUN apt-get remove -y build-essential pkg-config git

ENV PYTHONUNBUFFERED 1
#COPY ./backend/ /usr/src/app/
#WORKDIR /usr/src/app
ADD ./backend/requirements.txt /srv/requirements.txt
RUN pip3 install -r /srv/requirements.txt

WORKDIR /usr/src/app

ENTRYPOINT []
CMD []

