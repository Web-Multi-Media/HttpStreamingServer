[![Build Status](https://travis-ci.org/Web-Multi-Media/HttpStreamingServer.svg?branch=master)](https://travis-ci.org/Web-Multi-Media/HttpStreamingServer)

Intro
-------------------

The aim of the project is to create an easy to use http media presentation server based on Django Rest Framework and React. Support is currently limited to mp4/mkv container with H264/AAC content. 
Subtitles are added automatically if an adequate match is found (after a conversion from .srt to webvtt).


How to use
-------------------

#### Installation (Docker)

You'll need to have [`docker`](https://docs.docker.com/install/) and [`docker-compose`](https://docs.docker.com/compose/install/) installed.

#### RUN

Build the frontend:

    docker-compose -f docker-compose-prod.yml build

Run the server:

    docker-compose -f docker-compose-prod.yml up

Now the application should be accessible from your browser at `http://localhost:1337/streaming/`.


#### CONFIGURATION

The videos contained in the Videos/ folder are updated everytime the app is launched.

If you want to manually triggers an update, use the following command

    docker-compose -f docker-compose-prod.yml run --rm web python3 manage.py populatedb

If you want to reload videos while the app is running, you need to have a superuser created.

    docker-compose -f docker-compose-prod.yml run --rm web python3 manage.py createsuperuser

then go to `http://localhost:1337/admin/`, select all Videos and check 'reload Videos' actions.

The following variables can be configured in .env file:

    DJANGO_DATABASE_URL=postgres://postgres:password@db/streaming_server
    DJANGO_SECRET_KEY=fdj(re&lf87/qwm%jkiq78fdah346gsa
    POSTGRES_PASSWORD=password
    HTTPSTREAMING_HOST=www.foo.com


#### Build Process and Debug

See the /doc folder for more informations


