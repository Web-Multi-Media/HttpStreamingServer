[![Build Status](https://travis-ci.org/DerouineauNicolas/HttpStreamingServer.svg?branch=master)](https://travis-ci.org/DerouineauNicolas/HttpStreamingServer)

Intro
-------------------

This is a simple http media presentation server based on Django framework and Video-js.
Let's say you have one production server hosting videos (Apache/Nginx). This application will gather infos about those media and display them as a playlist.
Please note that this software assumes that you have local access to your video directory.

How to use
-------------------

#### Virtualenv & installation

From the root repository folder:

- `python3 -m venv ./venv`

- `source venv/bin/activate`

- `pip install django`


#### Configuration

- Edit `StreamingServer/settings.py` to modify `SERVER_VIDEO_DIR` and `REMOTE_BASE_URL`.

- Run the following command to create your db and fill it with the videos infos:

    `python3 manage.py migrate && python3 manage.py populatedb`

- Run the server:

    `python3 manage.py runserver`

- Now the application should be accessible from your browser at `http://localhost:8000/StreamServerApp/`.

