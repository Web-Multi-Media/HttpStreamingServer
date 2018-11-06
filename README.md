[![Build Status](https://travis-ci.org/DerouineauNicolas/HttpStreamingServer.svg?branch=master)](https://travis-ci.org/DerouineauNicolas/HttpStreamingServer)

Intro
-------------------

This is a simple http media presentation server based on Django framework and Video-js.
Let's say you have one production server hosting videos (Apache/Nginx). This application will gather infos about those media and display them as a playlist.
Please note that this software assumes that you have local access to your video directory.

How to use
-------------------

#### Installation (Docker)

You'll need to have [`docker`](https://docs.docker.com/install/) and [`docker-compose`](https://docs.docker.com/compose/install/) installed.

#### Configuration

Edit `StreamingServer/settings.py` to modify `SERVER_VIDEO_DIR` and `REMOTE_BASE_URL`.

The first time you load the application you will need to perform migrations:

    `docker-compose run --rm web python manage.py migrate`

You will have to fill the db with the video info:

    `docker-compose run --rm web python manage.py populatedb`

Run the server:

    `docker-compose up`

Now the application should be accessible from your browser at `http://localhost:8000/StreamServerApp/`.
