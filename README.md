[![Build Status](https://travis-ci.org/DerouineauNicolas/HttpStreamingServer.svg?branch=master)](https://travis-ci.org/DerouineauNicolas/HttpStreamingServer)

Intro
-------------------

This is a simple http media presentation server based on Django and Video-js.
It will display the Videos located in the Videos folder as a playlist in your webbrowser.

How to use
-------------------

#### Installation (Docker)

You'll need to have [`docker`](https://docs.docker.com/install/) and [`docker-compose`](https://docs.docker.com/compose/install/) installed.

#### RUN

The first time you load the application you will need to perform migrations:

    `docker-compose run --rm web python manage.py migrate`


Run the server:

    `docker-compose up`

Now the application should be accessible from your browser at `http://localhost:1337/StreamServerApp/`.


#### CONFIGURATION

The videos contained in the Videos/ folder are updated everytime the app is launched.

If you want to manually triggers an update, use the following command

    `docker-compose run --rm web python manage.py populatedb`
