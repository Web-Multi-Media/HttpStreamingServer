[![Build Status](https://travis-ci.org/DerouineauNicolas/HttpStreamingServer.svg?branch=master)](https://travis-ci.org/DerouineauNicolas/HttpStreamingServer)

Intro
-------------------

This is a simple http media presentation server based on Django and React.
It will display the Videos located in the Videos folder on the server side as a playlist in your webbrowser. Support is therefore limited to mp4 container with H264/AAC content.


How to use
-------------------

#### Installation (Docker)

You'll need to have [`docker`](https://docs.docker.com/install/) and [`docker-compose`](https://docs.docker.com/compose/install/) installed.

#### RUN

Build the frontend:

    `docker-compose -f docker-compose-prod.yml build`

Run the server:

    `docker-compose -f docker-compose-prod.yml up`

Now the application should be accessible from your browser at `http://localhost:1337/StreamServerApp/`.


#### CONFIGURATION

The videos contained in the Videos/ folder are updated everytime the app is launched.

If you want to manually triggers an update, use the following command

    `docker-compose run --rm web python manage.py populatedb`
