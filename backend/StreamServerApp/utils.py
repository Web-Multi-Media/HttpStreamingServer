# -*- coding: utf-8 -*-
"""Streaming server module utilies

This module provides functionalities to erase/update videos infos in the database

Todo:
    * Define how to interact with multiple servers
    * Update database only when needed.
"""

from StreamServerApp.models import Video, Folder
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

def pretty(d, indent=0):
    """ pretty print for nested dictionnary
    """
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))

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
    for root, directories, filenames in os.walk(video_path):
        idx += len(filenames)
        for filename in filenames:
            full_path = os.path.join(root, filename)

            if isfile(full_path) and (full_path.endswith(".mp4") or full_path.endswith(".mkv")):
                try:
                    # Print current working directory
                    video_infos = prepare_video(full_path, video_path)
                    if not video_infos:
                        print("Dict is Empty")
                        continue

                    v = Video(name=filename, \
                                            video_url="{}/{}".format(remote_url, video_infos['relative_path']),\
                                            video_codec=video_infos['video_codec_type'], audio_codec=video_infos['audio_codec_type'],\
                                            height=video_infos['video_height'], width=video_infos['video_width'], \
                                            thumbnail="{}/{}".format(remote_url, video_infos['thumbnail_relativepath']))
                    v.save()
                    folder, created = Folder.objects.get_or_create(path=root)
                    folder.save()
                    folder.videos.add(v)
                    folder.save()
                    
                except Exception as e:
                    print ("An error occured")
                    print (e)
                    continue


    print("{} videos were added to the database".format(str(get_DB_size())))

def prepare_video(full_path, video_path):
    """ # Create thumbnail, transmux if necessayr and get all the videos infos.
        Args:
        full_path: full path to the video
        video_path: full path to the video

        return: Dictionnary with video infos

        this functions will only add videos to the database if 
        they are encoded with h264/AAC codec
    """
    print(video_path)
    try:
        probe = ffmpeg.probe(full_path)
    except ffmpeg.Error as e:
        print(e.stderr, file=sys.stderr)
        raise

    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    if video_stream is None:
        print('No video stream found', file=sys.stderr)
        return {}

    video_codec_type = video_stream['codec_name']
    video_width = video_stream['width']
    video_height = video_stream['height']
    if 'duration' in video_stream:
        duration = float(video_stream['duration'])
    elif 'duration' in probe['format']:
        duration = float(probe['format']['duration'])

    audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
    if audio_stream is None:
        print('No audio stream found', file=sys.stderr)
        return {}

    audio_codec_type = audio_stream['codec_name']

    relative_path = os.path.relpath(full_path, video_path)

    if(("h264" in video_codec_type) and ("aac" in audio_codec_type)):
        #Thumbnail creation
        thumbnail_fullpath=os.path.splitext(full_path)[0]+'.jpg'
        thumbnail_relativepath=os.path.splitext(relative_path)[0]+'.jpg'
        subprocess.run(["ffmpeg", "-n", "-ss", str(duration/2.0), "-i", full_path,\
        "-an", "-vf", "scale=320:-1", \
        "-vframes", "1", thumbnail_fullpath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        #if file is mkv, transmux to mp4
        if(full_path.endswith(".mkv")):
            temp_mp4 = os.path.splitext(full_path)[0]+'.mp4'
            cmd = ["ffmpeg", "-n", "-i", full_path, "-codec", "copy", temp_mp4]
            try:
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError as e:
                print(e.returncode)
                print(e.cmd)
                print(e.output)
                raise
            #remove old mkv file
            os.remove(full_path)
            relative_path = os.path.splitext(relative_path)[0]+'.mp4'
    else:
        #Input is not h264, let's skip it
        return {}

    return {'relative_path': relative_path, 'video_codec_type': video_codec_type, \
            'audio_codec_type': audio_codec_type, 'video_height': video_height,\
            'video_width': video_width, 'thumbnail_relativepath': thumbnail_relativepath }

def populate_db_from_remote_server(remotePath, ListOfVideos):
    """ # tobeDone
       ListOfVideos could be provided through an API Call
    """
