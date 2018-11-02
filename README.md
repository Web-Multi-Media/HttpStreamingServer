[![Build Status](https://travis-ci.org/DerouineauNicolas/HttpStreamingServer.svg?branch=master)](https://travis-ci.org/DerouineauNicolas/HttpStreamingServer)

Intro
-------------------

This is a simple http media presentation server based on Django framework and Video-js.
Let's say you have one production server hosting videos (Apache/Nginx). This application will gather infos about those media and display them as a playlist.
Please note that this software assumes that you have local access to your video directory.

How to use
-------------------
1, pip3 install django

2, Edit StreamingServer/settings.py to modify SERVER_VIDEO_DIR and REMOTE_BASE_URL.

3, Run the following command to create your db and fill it with the videos infos.

python3 manage.py migrate && python3 manage.py populatedb

4, Run the server

python3 manage.py runserver


