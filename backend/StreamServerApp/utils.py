# -*- coding: utf-8 -*-
"""Streaming server module utilies

This module provides functionalities to erase/update videos infos in the database

Todo:
    * Define how to interact with multiple servers
    * Update database only when needed.
"""
import os
import sys
import string
from os.path import isfile, join
import ffmpeg
import subprocess
import traceback
from datetime import timedelta
import subliminal

from StreamServerApp.models import Video, Series, Movie
from StreamingServer.settings import customstderr, customstdout
from StreamServerApp.subtitles import get_subtitles, init_cache


def delete_DB_Infos():
    """ delete all videos, movies and series in the db
    """
    Video.objects.all().delete()
    Movie.objects.all().delete()
    Series.objects.all().delete()


def get_num_videos():
    """ Return the number of videos in the db
    """
    return Video.objects.count()


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
    init_cache()
    video_path = base_path
    idx = 0
    count_series = 0
    count_movies = 0

    print ("Get videos infos in dir: {} ".format(video_path))

    for root, directories, filenames in os.walk(video_path):
        idx += len(filenames)
        for filename in filenames:
            full_path = os.path.join(root, filename)

            if isfile(full_path) and (full_path.endswith(".mp4") or full_path.endswith(".mkv")):
                try:
                    # Print current working directory
                    print ("Current working dir : %s" % root)
                    video_infos = prepare_video(full_path, video_path, root, remote_url)
                    if not video_infos:
                        print("Dict is Empty")
                        continue

                    v = Video(name=filename, video_folder = root, \
                                            video_url=video_infos['remote_video_url'],\
                                            video_codec=video_infos['video_codec_type'], audio_codec=video_infos['audio_codec_type'],\
                                            height=video_infos['video_height'], width=video_infos['video_width'], \
                                            thumbnail=video_infos['remote_thumbnail_url'], \
                                            fr_subtitle_url=video_infos['fr_subtitles_remote_path'], ov_subtitle_url = video_infos['ov_subtitles_remote_path'],\
                                            en_subtitle_url=video_infos['en_subtitles_remote_path'])
                    
                    # parse movie or series, episode & season
                    video_type_and_info = get_video_type_and_info(filename)

                    if video_type_and_info:
                        if video_type_and_info['type'] == 'Series':
                            series, created = Series.objects.get_or_create(title=video_type_and_info['title'],
                                                                           defaults={'thumbail': video_infos['remote_thumbnail_url']})
                            v.series = series
                            v.season = video_type_and_info['season']
                            v.episode = video_type_and_info['episode']
                            if created:
                                count_series += 1

                        elif video_type_and_info['type'] == 'Movie':
                            movie, created = Movie.objects.get_or_create(title=video_type_and_info['title'])
                            v.movie = movie
                            if created:
                                count_movies += 1
                                
                    v.save()

                except Exception as ex:
                    print ("An error occured")
                    traceback.print_exception(type(ex), ex, ex.__traceback__)
                    continue

    print("{} videos were added to the database".format(get_num_videos()))
    print('{} series and {} movies were created'.format(count_series, count_movies))


def prepare_video(video_full_path, video_path, video_dir, remote_url):
    """ # Create thumbnail, transmux if necessayr and get all the videos infos.
        Args:
        full_path: full path to the video (eg: /Videos/folder1/video.mp4)
        video_path: path to the video basedir (eg: /Videos/)
        video_dir: path to the video dir (eg: /Videos/folder1/)

        return: Dictionnary with video infos

        this functions will only add videos to the database if 
        they are encoded with h264/AAC codec
    """
    print(video_full_path)
    print(video_path)
    try:
        probe = ffmpeg.probe(video_full_path)
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
        #At the moment, if the input video has no audio, it's not added to the database. 
        print('No audio stream found', file=sys.stderr)
        return {}

    ov_subtitles = False
    subtitles_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'subtitle'), None)
    if subtitles_stream is not None:
        print('Found Subtitles in the input stream')
        ov_subtitles = True

    audio_codec_type = audio_stream['codec_name']

    relative_path = os.path.relpath(video_full_path, video_path)
    if(("h264" in video_codec_type) and ("aac" in audio_codec_type)):
        #Thumbnail creation
        thumbnail_fullpath=os.path.splitext(video_full_path)[0]+'.jpg'
        thumbnail_relativepath=os.path.splitext(relative_path)[0]+'.jpg'
        if(os.path.isfile(thumbnail_fullpath) == False):
            subprocess.run(["ffmpeg", "-ss", str(duration/2.0), "-i", video_full_path,
                            "-an", "-vf", "scale=320:-1",
                            "-vframes", "1", thumbnail_fullpath], stdout=customstdout, stderr=customstderr)

        #if file is mkv, transmux to mp4
        if(video_full_path.endswith(".mkv")):
            temp_mp4 = os.path.splitext(video_full_path)[0]+'.mp4'
            if(os.path.isfile(temp_mp4) == False):
                cmd = ["ffmpeg", "-i", video_full_path,
                       "-codec", "copy", temp_mp4]
                try:
                    subprocess.run(cmd, stdout=customstdout,
                                   stderr=customstderr)
                except subprocess.CalledProcessError as e:
                    print(e.returncode)
                    print(e.cmd)
                    print(e.output)
                    raise
            #remove old mkv file
            os.remove(video_full_path)
            relative_path = os.path.splitext(relative_path)[0]+'.mp4'
            video_full_path = temp_mp4

        subtitles_full_path = get_subtitles(video_full_path, ov_subtitles)
        fr_subtitles_remote_path = ''
        if(subtitles_full_path[0]):
            fr_subtitles_relative_path = os.path.relpath(subtitles_full_path[0], video_path)
            fr_subtitles_remote_path = os.path.join(remote_url, fr_subtitles_relative_path)

        en_subtitles_remote_path = ''
        if(subtitles_full_path[1]):
            en_subtitles_relative_path = os.path.relpath(subtitles_full_path[1], video_path)
            en_subtitles_remote_path = os.path.join(remote_url, en_subtitles_relative_path)

        ov_subtitles_remote_path = ''
        if(subtitles_full_path[2]):
            ov_subtitles_relative_path = os.path.relpath(subtitles_full_path[2], video_path)
            ov_subtitles_remote_path = os.path.join(remote_url, ov_subtitles_relative_path)

    else:
        #Input is not h264, let's skip it
        return {}

    remote_video_url = os.path.join(remote_url, relative_path)
    remote_thumbnail_url = os.path.join(remote_url, thumbnail_relativepath)

    return {'remote_video_url': remote_video_url, 'video_codec_type': video_codec_type, \
            'audio_codec_type': audio_codec_type, 'video_height': video_height,\
            'video_width': video_width, 'remote_thumbnail_url': remote_thumbnail_url,\
             'fr_subtitles_remote_path':fr_subtitles_remote_path, 'en_subtitles_remote_path':en_subtitles_remote_path,
             'ov_subtitles_remote_path':ov_subtitles_remote_path}


def populate_db_from_remote_server(remotePath, ListOfVideos):
    """ # tobeDone
       ListOfVideos could be provided through an API Call
    """


def get_video_type_and_info(video_path):
    """ # Uses subliminal to parse information from filename.
    
    Subliminal tells us if the video is a serie or not.
    If not, we assume it to be a movie, which is not necesarly the case (e.g. documentary, simple video).
    We use string.capwords() on title strings for consistency of capitalization.
    
    Args:
    video_path: full path to the video (eg: /Videos/folder1/video.mp4)

    Returns: dict containing video type and info

    """
    video = subliminal.Video.fromname(video_path)
    if hasattr(video, 'series'):
        return {
            'type': 'Series',
            'title': string.capwords(video.series),
            'season': video.season,
            'episode': video.episode,
        }
    elif hasattr(video, 'title'):
        return {
            'type': 'Movie',
            'title': string.capwords(video.title),
        }
