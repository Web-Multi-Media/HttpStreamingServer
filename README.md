[![Build Status](https://travis-ci.org/Web-Multi-Media/HttpStreamingServer.svg?branch=master)](https://travis-ci.org/Web-Multi-Media/HttpStreamingServer)

Intro
-------------------

This is a simple http media presentation server based on Django and React.
It will display the Videos located in the Videos folder on the server side as a playlist in your webbrowser. Support is therefore limited to mp4 container with H264/AAC content. In case mkv files with H264/AAC codecs are present in the Videos folder, they will be transmuxed to mp4 without reencoding.
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

#### Build Process and Debug

See the /doc folder for more informations


