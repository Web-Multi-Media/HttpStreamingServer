
FROM python:3.6

RUN apt-get update -y && apt-get install -y ffmpeg 

ENV PYTHONUNBUFFERED 1
COPY . /usr/src/app/
WORKDIR /usr/src/app

RUN pip3 install -r requirements.txt
