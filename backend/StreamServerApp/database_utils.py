# -*- coding: utf-8 -*-
"""Streaming server module utilies

This module provides functionalities to erase/update videos infos in the database

Todo:
    * Define how to interact with multiple servers
"""
import os
import sys
import string
from os.path import isfile, join
import ffmpeg
import traceback
import subliminal
from django.db import transaction
import re

from StreamServerApp.models import Video, Series, Movie, Subtitle
from StreamServerApp.subtitles import init_cache
from StreamServerApp.media_processing import transmux_to_mp4, generate_thumbnail
from StreamServerApp.media_management.encoder import h264_encoder, aac_encoder, extract_audio
from StreamServerApp.media_management.dash_packager import dash_packager
from StreamServerApp.media_management.fileinfo import createfileinfo, readfileinfo
from StreamServerApp.tasks import get_subtitles_async


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
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


def populate_db_from_local_folder(base_path, remote_url, keep_files=False):
    """ # create all the videos infos in the database
        Args:
        remote_url: baseurl for video access on the server
        base_path: Local Folder where the videos are stored
        keep_files: keep video files instead of deleting it in case of conversion


        this functions will only add videos to the database if
        they are encoded with h264 codec
    """
    init_cache()
    video_path = base_path
    idx = 0
    count_series = 0
    count_movies = 0

    for root, directories, filenames in os.walk(video_path):
        idx += len(filenames)
        for filename in filenames:
            full_path = os.path.join(root, filename)

            if isfile(full_path) and (full_path.endswith(".mp4")
                                      or full_path.endswith(".mkv")
                                      or full_path.endswith(".avi")):
                try:
                    # Atomic transaction in order to make all occur or nothing occurs in case of exception raised
                    with transaction.atomic():
                        retValue = add_one_video_to_database(
                            full_path, video_path, root, remote_url, filename,
                            keep_files)
                        if retValue == 1:
                            count_movies += 1
                        elif retValue == 2:
                            count_series += 1

                except Exception as ex:
                    print("An error occured")
                    traceback.print_exception(type(ex), ex, ex.__traceback__)
                    continue
            elif isfile(full_path) and (full_path.endswith(".mpd")):
                try:
                    # Atomic transaction in order to make all occur or nothing occurs in case of exception raised
                    with transaction.atomic():
                        retValue = add_one_manifest_to_database(
                            full_path, video_path, root, remote_url, filename,
                            keep_files)
                        if retValue == 1:
                            count_movies += 1
                        elif retValue == 2:
                            count_series += 1

                except Exception as ex:
                    print("An error occured")
                    traceback.print_exception(type(ex), ex, ex.__traceback__)
                    continue

    print("{} videos were added to the database".format(get_num_videos()))
    print('{} series and {} movies were created'.format(
        count_series, count_movies))


def update_db_from_local_folder(base_path, remote_url, keep_files=False):
    """ #  Update  the videos infos in the database
        Args:
        remote_url: baseurl for video access on the server
        base_path: Local Folder where the videos are stored

        this functions will only add videos to the database if
        they are encoded with h264 codec
    """
    video_path = base_path
    idx = 0
    count_series = 0
    count_movies = 0

    database_old_files = Video.objects.values_list('video_folder', 'id')

    old_path_set = set()

    #We check here if old database files are still present on filesystem, if not, delete from db
    video_ids_to_delete = []
    for old_files_path, old_video_id in database_old_files:
        if os.path.isfile(old_files_path) is False:
            print(old_files_path + "will be deleted")
            video_ids_to_delete.append(old_video_id)
        else:
            old_path_set.add(old_files_path)

    Video.objects.filter(pk__in=video_ids_to_delete).delete()

    #Remove empty Series/Movies dataset
    Series.objects.filter(video=None).delete()
    Movie.objects.filter(video=None).delete()

    num_video_before = get_num_videos()

    for root, directories, filenames in os.walk(video_path):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            if full_path in old_path_set:
                print(full_path + " is already in db, skip it")
                continue

            if isfile(full_path) and (full_path.endswith(".mp4")
                                      or full_path.endswith(".mkv")
                                      or full_path.endswith(".avi")):
                try:
                    # Atomic transaction in order to make all occur or nothing occurs in case of exception raised
                    with transaction.atomic():
                        created = add_one_video_to_database(
                            full_path, video_path, root, remote_url, filename,
                            keep_files)
                        if created == 1:
                            count_movies += 1
                        elif created == 2:
                            count_series += 1

                except Exception as ex:
                    print("An error occured")
                    traceback.print_exception(type(ex), ex, ex.__traceback__)
                    continue
            elif isfile(full_path) and (full_path.endswith(".mpd")):
                try:
                    # Atomic transaction in order to make all occur or nothing occurs in case of exception raised
                    with transaction.atomic():
                        retValue = add_one_manifest_to_database(
                            full_path, video_path, root, remote_url, filename,
                            keep_files)
                        if retValue == 1:
                            count_movies += 1
                        elif retValue == 2:
                            count_series += 1

                except Exception as ex:
                    print("An error occured")
                    traceback.print_exception(type(ex), ex, ex.__traceback__)
                    continue

    num_video_after = get_num_videos()

    print("{} videos were added to the database".format(num_video_after -
                                                        num_video_before))
    print('{} series and {} movies were created'.format(
        count_series, count_movies))


def add_one_video_to_database(full_path,
                              video_path,
                              root,
                              remote_url,
                              filename,
                              keep_files=False):
    """ # create infos in the database for one video

        Args:
        full_path: absolue path to the video
        video_path: relative (to root) basepath (ie directory) containing video
        root: absolute path to directory containing all the videos
        remote_url: baseurl for video access on the server
        keep_files: Keep files in case of convertion

        return 0 if noseries/movies was created, 1 if a movies was created, 2 if a series was created

    """
    # Print current working directory
    print("Current working dir : %s" % root)
    video_infos = prepare_video(full_path, video_path, root, remote_url,
                                keep_files)
    if not video_infos:
        print("video infos are empty, don't add to database")
        return 0

    v = Video(
        name=filename,
        video_folder=video_infos['mpd_path'],
        video_url=video_infos['remote_video_url'],
        video_codec=video_infos['video_codec_type'],
        audio_codec=video_infos['audio_codec_type'],
        height=video_infos['video_height'],
        width=video_infos['video_width'],
        thumbnail=video_infos['remote_thumbnail_url'],
    )

    # parse movie or series, episode & season
    return_value = 0
    video_type_and_info = get_video_type_and_info(filename)

    if video_type_and_info:
        if video_type_and_info['type'] == 'Series':
            series, created = Series.objects.get_or_create(
                title=video_type_and_info['title'],
                defaults={'thumbnail': video_infos['remote_thumbnail_url']})
            v.series = series
            v.season = video_type_and_info['season']
            v.episode = video_type_and_info['episode']

            if created:
                return_value = 2

        elif video_type_and_info['type'] == 'Movie':
            movie, created = Movie.objects.get_or_create(
                title=video_type_and_info['title'])
            v.movie = movie

            if created:
                return_value = 1

        v.save()

        #we use oncommit because autocommit is not enabled.
        transaction.on_commit(lambda: get_subtitles_async.delay(
            v.id, video_infos['has_ov_subtitle'], video_path, remote_url))

    return return_value


def add_one_manifest_to_database(full_path,
                                 video_path,
                                 root,
                                 remote_url,
                                 filename,
                                 keep_files=False):
    """ # create infos in the database for one manifest

        Args:
        full_path: absolue path to the video
        video_path: relative (to root) basepath (ie directory) containing video
        root: absolute path to directory containing all the videos
        remote_url: baseurl for video access on the server
        keep_files: Keep files in case of convertion

        return 0 if noseries/movies was created, 1 if a movies was created, 2 if a series was created

    """
    # Print current working directory
    print("Current working dir : %s" % root)
    video_infos = []
    fileinfos_path = "{}/fileinfo.json".format(os.path.split(full_path)[0])
    if os.path.isfile(fileinfos_path):
        video_infos = readfileinfo(fileinfos_path)
        if not video_infos:
            print("video infos are empty, don't add to database")
            return 0
    else:
        return 0

    print("video_infos = {}".format(video_infos))

    filename = os.path.split(video_infos['video_full_path'])[1]

    print("filename = {}".format(filename))

    v = Video(
        name=filename,
        video_folder=full_path,
        video_url=video_infos['remote_video_url'],
        video_codec=video_infos['video_codec_type'],
        audio_codec=video_infos['audio_codec_type'],
        height=video_infos['video_height'],
        width=video_infos['video_width'],
        thumbnail=video_infos['remote_thumbnail_url'],
    )

    # parse movie or series, episode & season
    return_value = 0
    video_type_and_info = get_video_type_and_info(filename)

    if video_type_and_info:
        if video_type_and_info['type'] == 'Series':
            series, created = Series.objects.get_or_create(
                title=video_type_and_info['title'],
                defaults={'thumbnail': video_infos['remote_thumbnail_url']})
            v.series = series
            v.season = video_type_and_info['season']
            v.episode = video_type_and_info['episode']

            if created:
                return_value = 2

        elif video_type_and_info['type'] == 'Movie':
            movie, created = Movie.objects.get_or_create(
                title=video_type_and_info['title'])
            v.movie = movie

            if created:
                return_value = 1

        v.save()

        #we use oncommit because autocommit is not enabled.
        transaction.on_commit(lambda: get_subtitles_async.delay(
            v.id, video_infos['has_ov_subtitle'], video_path, remote_url))

    return return_value


def populate_db_from_remote_server(remotePath, ListOfVideos):
    """ # tobeDone
       ListOfVideos could be provided through an API Call
    """


def prepare_video(video_full_path,
                  video_path,
                  video_dir,
                  remote_url,
                  keep_files=False):
    """ # Create thumbnail, transmux if necessayr and get all the videos infos.
        Args:
        full_path: full path to the video (eg: /Videos/folder1/video.mp4)
        video_path: path to the video basedir (eg: /Videos/)
        video_dir: path to the video dir (eg: /Videos/folder1/)
        keep_files: Keep original files in case of convertion

        return: Dictionnary with video infos

        this functions will only add videos to the database if
        they are encoded with h264/AAC codec
    """
    print("processing {}".format(video_full_path))
    try:
        probe = ffmpeg.probe(video_full_path)
    except ffmpeg.Error as e:
        print(e.stderr, file=sys.stderr)
        raise

    video_stream = next(
        (stream
         for stream in probe['streams'] if stream['codec_type'] == 'video'),
        None)
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

    audio_stream = next(
        (stream
         for stream in probe['streams'] if stream['codec_type'] == 'audio'),
        None)
    if audio_stream is None:
        #At the moment, if the input video has no audio, it's not added to the database.
        print('No audio stream found', file=sys.stderr)
        return {}

    ov_subtitles = False
    subtitles_stream = next(
        (stream
         for stream in probe['streams'] if stream['codec_type'] == 'subtitle'),
        None)
    if subtitles_stream is not None:
        print('Found Subtitles in the input stream')
        ov_subtitles = True

    audio_codec_type = audio_stream['codec_name']
    audio_elementary_stream_path = "{}.m4a".format(
        os.path.splitext(video_full_path)[0])
    video_elementary_stream_path_480 = "{}_480.264".format(
        os.path.splitext(video_full_path)[0])
    video_elementary_stream_path_720 = "{}_720.264".format(
        os.path.splitext(video_full_path)[0])
    dash_output_directory = os.path.splitext(video_full_path)[0]
    temp_mpd = "{}/playlist.mpd".format(dash_output_directory)

    if "aac" in audio_codec_type:
        extract_audio(video_full_path, audio_elementary_stream_path)
    else:
        aac_encoder(video_full_path, audio_elementary_stream_path)

    h264_encoder(
        video_full_path,
        video_elementary_stream_path_720, 720, 1800000)
    h264_encoder(
        video_full_path,
        video_elementary_stream_path_480, 480, 800000)

    relative_path = os.path.relpath(video_full_path, video_path)

    if not os.path.exists(dash_output_directory):
        os.mkdir(dash_output_directory)

    #Thumbnail creation
    thumbnail_fullpath = "{}/thumbnail.jpeg".format(dash_output_directory)

    thumbnail_relativepath = os.path.relpath(thumbnail_fullpath, video_path)
    if (os.path.isfile(thumbnail_fullpath) is False):
        generate_thumbnail(video_full_path, duration, thumbnail_fullpath)

    #Dash_packaging
    dash_packager(video_elementary_stream_path_480, video_elementary_stream_path_720, audio_elementary_stream_path,
                  dash_output_directory)

    os.remove(video_elementary_stream_path_720)
    os.remove(video_elementary_stream_path_480)
    os.remove(audio_elementary_stream_path)

    if not keep_files:
        os.remove(video_full_path)

    relative_path = os.path.relpath(temp_mpd, video_path)

    remote_video_url = os.path.join(remote_url, relative_path)
    remote_thumbnail_url = os.path.join(remote_url, thumbnail_relativepath)
    video_info = {
        'remote_video_url': remote_video_url,
        'video_codec_type': video_codec_type,
        'audio_codec_type': audio_codec_type,
        'video_height': video_height,
        'video_width': video_width,
        'remote_thumbnail_url': remote_thumbnail_url,
        'has_ov_subtitle': ov_subtitles,
        'video_full_path': video_full_path,
        'mpd_path': temp_mpd
    }

    #File info creation
    fileinfo_path = "{}/fileinfo.json".format(dash_output_directory)
    createfileinfo(fileinfo_path, video_info)

    return video_info


def get_video_type_and_info(video_path):
    """ # Uses subliminal to parse information from filename.

    Subliminal tells us if the video is a serie or not.
    If not, we assume it to be a movie, which is not necesarly the case (e.g. documentary, simple video).
    We use string.capwords() on title strings for consistency of capitalization.
    The subliminal fromname function as a bug when the input string begins with 1-, as a quick fix, we use a regular expression to
    get rid of the problematic characters. A future fix coulb be to be use imdb api for disambiguation.

    Args:
    video_path: full path to the video (eg: /Videos/folder1/video.mp4)

    Returns: dict containing video type and info

    """
    filename = os.path.basename(video_path)
    if re.match(r'(\d*(\-|\.) .*)', filename):
        filename = re.sub(r'(\d*(\-|\.) )', '', filename, 1)
    try:
        video = subliminal.Video.fromname(filename)
    except ValueError:
        #This usually happens when there is not enough data for subliminal to guess.
        return {
            'type': 'Movie',
            'title': string.capwords(filename),
        }

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
