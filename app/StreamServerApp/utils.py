# -*- coding: utf-8 -*-
"""Streaming server module utilies

This module provides functionalities to erase/update videos infos in the database

Todo:
    * Define how to interact with multiple servers
    * Update database only when needed.
"""

from StreamServerApp.models import Video
import os
from os.path import isfile, join
import ffmpeg
import subprocess

def delete_DB_Infos():
    """ delete all videos infos in the db
    """
    Video.objects.all().delete()

def get_DB_size():
    """ Return db size
    """
    return len(Video.objects.all())

def populate_db_from_local_folder(base_path, remote_url):
    """ # create all the videos infos in the database
        Args:
        remote_url: baseurl for video access on the server
        base_path: Local Folder where the videos are stored

        this functions will only add videos to the database if 
        they are encoded with h264/AAC codec
    """
    video_path = base_path
    idx = 0
    print ("Get videos infos in dir: {} ".format(video_path))
    for root, directories, filenames in os.walk(video_path):
        idx += len(filenames)
        for filename in filenames:
            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, video_path)
            print(full_path)
            print(relative_path)
            if isfile(full_path) and (full_path.endswith(".mp4")):
                try:
                    probe = ffmpeg.probe(full_path)
                except ffmpeg.Error as e:
                    print(e.stderr, file=sys.stderr)
                    continue

                video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
                if video_stream is None:
                    print('No video stream found', file=sys.stderr)
                    continue

                video_codec_type = video_stream['codec_name']
                video_width = video_stream['width']
                video_height = video_stream['height']
                duration = float(video_stream['duration'])

                audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
                if audio_stream is None:
                    print('No video stream found', file=sys.stderr)
                    continue

                audio_codec_type = audio_stream['codec_name']



                if(full_path.endswith(".mp4") and ("h264" in video_codec_type) and ("aac" in audio_codec_type)):
                    thumbnail_fullpath=os.path.splitext(full_path)[0]+'.jpg'
                    thumbnail_relativepath=os.path.splitext(relative_path)[0]+'.jpg'
                    subprocess.run(["ffmpeg", "-ss", str(duration/2), "-i", full_path, "-an", "-vf", "select=eq(pict_type\,I),scale=320:-1", "-vframes", "1", thumbnail_fullpath])
                    v = Video(name=filename, baseurl="{}/{}".format(remote_url, relative_path),\
                                        video_codec=video_codec_type, audio_codec=audio_codec_type,\
                                        height=video_height, width=video_width, thumbnail="{}/{}".format(remote_url, thumbnail_relativepath))
                    v.save()



    print("{} videos were added to the database".format(str(get_DB_size())))

def populate_db_from_remote_server(remotePath, ListOfVideos):
    """ # tobeDone
       ListOfVideos could be provided through an API Call
    """
