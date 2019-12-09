
FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
RUN apt-get install -y software-properties-common
RUN apt-get install -y python3-software-properties
RUN apt-get install -y x264 x265 ffmpeg

ENV PYTHONUNBUFFERED 1
COPY . /usr/src/app/
WORKDIR /usr/src/app

RUN pip3 install -r requirements.txt
