
FROM node:8

RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential \
    software-properties-common python3-software-properties \
    x264 x265 ffmpeg && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1
COPY . /usr/src/app/
WORKDIR /usr/src/app

RUN pip3 install -r requirements.txt
