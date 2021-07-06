[![Build Status](https://travis-ci.com/Web-Multi-Media/HttpStreamingServer.svg?branch=master)](https://travis-ci.com/Web-Multi-Media/HttpStreamingServer)

Intro
-------------------
This project is a video presentation server based on Django Rest Framework and React. It provides automatic video indexing and classification.

![](doc/preview.jpeg )


Support is currently limited to H264 encoded content.
Subtitles are added automatically if an adequate match is found. You can also upload you own subtitle or resync existing ones.


How to use
-------------------

#### Installation (Docker)

You'll need to have [`docker`](https://docs.docker.com/install/) and [`docker-compose`](https://docs.docker.com/compose/install/) installed.

#### RUN

Pull the images:

    docker-compose -f docker-compose-prod.yml pull

Migrate the database:

    docker-compose -f docker-compose-prod.yml run --rm web python3 manage.py migrate

Populate the database:

    docker-compose -f docker-compose-prod.yml run --rm web ./wait-for-it.sh db:5432 -- python3 manage.py populatedb

Run the server:

    docker-compose -f docker-compose-prod.yml up

Now the application should be accessible from your browser at `http://localhost:1337/streaming/`.

A built-in torrent server is available at: `http://localhost:1337/transmission/web/`


#### CONFIGURATION

Change torrent admin password:

    docker-compose -f docker-compose-prod.yml run --rm nginx htpasswd -c /usr/torrent/.htpasswd user1

The videos contained in the Videos/ folder are indexed everytime the populatedb command is launched.

If you want to trigger an update, use the following command

    docker-compose -f docker-compose-prod.yml run --rm web python3 manage.py updatedb

If you want to manually modify the data, you can access the admin page with a superuser account. For that, create one with the following command.

    docker-compose -f docker-compose-prod.yml run --rm web python3 manage.py createsuperuser

then go to `http://localhost:1337/admin/`.

The following variables can be configured in .env file:

    DJANGO_DATABASE_URL=postgres://postgres:password@db/streaming_server
    DJANGO_SECRET_KEY=fdj(re&lf87/qwm%jkiq78fdah346gsa
    POSTGRES_PASSWORD=password
    HTTPSTREAMING_HOST=www.foo.com
    SENTRY_DSN=https://foo.ingest.sentry.io/bar
    REACT_APP_SENTRY_DSN=https://foo.ingest.sentry.io/bar


#### Contributing

See the /doc folder for more informations on how to run a debug version of this app.


