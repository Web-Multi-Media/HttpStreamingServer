[![Build Status](https://travis-ci.org/DerouineauNicolas/HttpStreamingServer.svg?branch=master)](https://travis-ci.org/DerouineauNicolas/HttpStreamingServer)

Intro
-------------------

This is a simple http media presentation server based on Django and Video-js.
It will display the Videos located in the Videos folder as a playlist in your webbrowser.

How to use
-------------------

#### Installation (Docker)

You'll need to have [`docker`](https://docs.docker.com/install/) and [`docker-compose`](https://docs.docker.com/compose/install/) installed.

#### Configuration

The first time you load the application you will need to perform migrations:

    `docker-compose run --rm web python manage.py migrate`

You will have to fill the db with the video info:

    `docker-compose run --rm web python manage.py populatedb`

Run the server:

    `docker-compose up`

Now the application should be accessible from your browser at `http://localhost:1337/StreamServerApp/`.
