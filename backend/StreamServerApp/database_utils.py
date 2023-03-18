# -*- coding: utf-8 -*-
"""Streaming server module utilies

This module provides functionalities to erase/update videos infos in the database

Todo:
    * Define how to interact with multiple servers
"""
import os

from os.path import isfile, join

import traceback

from django.db import transaction

from celery import shared_task
from django.core.cache import cache

from StreamServerApp.models import Video, Series, Movie, Subtitle
from StreamServerApp.subtitles import init_cache

from StreamServerApp.media_management.fileinfo import createfileinfo, readfileinfo
from StreamServerApp.media_processing import prepare_video, get_video_type_and_info
from StreamServerApp.tasks import get_subtitles_async
from StreamingServer import settings


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


def update_db_from_local_folder(base_path, remote_url, keep_files=False):
    """ #  Update  the videos infos in the database
        Args:
        remote_url: baseurl for video access on the server
        base_path: Local Folder where the videos are stored

        this functions will only add videos to the database if
        they are encoded with h264 codec
    """

    init_cache()
    video_path = base_path
    idx = 0
    count_series = 0
    count_movies = 0

    database_old_files = Video.objects.values_list('video_folder', 'id')

    old_path_set = set()

    cache.set("processing_state", "cleaning old files", timeout=None)

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

    cache.set("processing_state", "finished", timeout=None)
    cache.delete("audio_total_duration")
    cache.delete("video_frames")
    cache.delete("processing_file")


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
        audio_path=video_infos['audio_path'],
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
        for ov_subtitle_path in video_infos["ov_subtitles"]:
            ov_sub = Subtitle()
            webvtt_subtitles_relative_path = os.path.relpath(
                ov_subtitle_path, video_path)
            ov_sub.webvtt_subtitle_url = os.path.join(
                remote_url, webvtt_subtitles_relative_path)
            ov_sub.vtt_path = ov_subtitle_path
            ov_sub.language = Subtitle.OV
            ov_sub.video_id = v
            ov_sub.save()

        #we use oncommit because autocommit is not enabled.
        transaction.on_commit(lambda: get_subtitles_async.delay(
            v.id, video_path, remote_url))

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
            v.id, video_path, remote_url))

    return return_value


def populate_db_from_remote_server(remotePath, ListOfVideos):
    """ # tobeDone
       ListOfVideos could be provided through an API Call
    """



@shared_task
def update_db_from_local_folder_async(keep_files):
    update_db_from_local_folder(settings.VIDEO_ROOT, settings.VIDEO_URL, keep_files)
    update_db_from_local_folder("/usr/torrent/", "/torrents/", keep_files)
    cache.set("is_updating", "false", timeout=None)
    return 0
