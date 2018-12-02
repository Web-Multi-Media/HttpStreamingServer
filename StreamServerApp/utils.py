# -*- coding: utf-8 -*-
"""Streaming server module utilies

This module provides functionalities to erase/update videos infos in the database

Todo:
    * Define how to interact with multiple servers
    * Update database only when needed.
    * Remove hardcoded name for search value.
"""

from StreamServerApp.models import Video
import os
from os.path import isfile, join

VIDEO_NAMES = ['canard', 'cochon', 'singe']

def delete_DB_Infos():
    """ delete all videos infos in the db
    """
    Video.objects.all().delete()

def get_DB_size():
    """ Return db size
    """
    return len(Video.objects.all())

def populate_db_from_local_folder(remote_path, base_path):
    """ # create all the videos infos in the database
        Args:
        remotePath: baseurl for video access on the server
        basepPath: Local Folder where the videos are stored
    """
    video_path = base_path
    idx = 0
    for root, directories, filenames in os.walk(video_path):
        idx += len(filenames)
        for filename in filenames:
            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, video_path)
            if isfile(full_path) and full_path.endswith(".mp4"):
                v = Video(name=VIDEO_NAMES[idx % 3], baseurl="{}/{}".format(remote_path, relative_path))
                v.save()

def populate_db_from_remote_server(remotePath, ListOfVideos):
    """ # tobeDone
       ListOfVideos could be provided through an API Call
    """
