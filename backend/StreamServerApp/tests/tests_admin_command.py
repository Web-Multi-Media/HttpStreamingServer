import os
import json
import shutil
from os.path import isfile
from django.urls import reverse
from django.core.management import call_command
from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from StreamServerApp.database_utils import get_num_videos, get_video_type_and_info
from StreamServerApp.models import Video, Series, Movie, UserVideoHistory, Subtitle
from StreamServerApp.media_processing import extract_subtitle, generate_thumbnail
from StreamServerApp.subtitles import get_subtitles

from StreamServerApp.database_utils import delete_DB_Infos, populate_db_from_local_folder, update_db_from_local_folder


class CommandsTestCase(TestCase):
    def test_database_populate_command(self):
        " Test database creation."

        args = []
        opts = {}
        #call_command('populatedb', *args, **opts)
        populate_db_from_local_folder("/usr/src/app/Videos/folder1/", settings.VIDEO_URL)
        # a bit of a mess here to make sure to count only files in all folders...
        files_in_videos_folders = [[os.path.join(root, file) for file in files] for root, _, files in os.walk("/usr/src/app/Videos/folder1/")]
        video_files = [filename for sublist in files_in_videos_folders for filename in sublist  # flatten nested list
                       if isfile(filename) and (filename.endswith(".mp4") or filename.endswith(".mkv"))]
        self.assertEqual(get_num_videos(), len(video_files))

    def test_movies_series_added_to_db(self):
        # We check that only one Series instance is created (2 bing band theory episodes)
        # and 4 Movie instances are created.
        # We also check that the video fields are set correctly.
        #call_command('populatedb')
        populate_db_from_local_folder("/usr/src/app/Videos/folder1/", settings.VIDEO_URL)

        self.assertEqual(Series.objects.count(), 1)
        self.assertEqual(Movie.objects.count(), 1)

        video = Video.objects.get(name='The.Big.Bang.Theory.S05E19.HDTV.x264-LOL.mp4')
        series = Series.objects.first()
        self.assertEqual(video.episode, 19)
        self.assertEqual(video.season, 5)
        self.assertEqual(video.series, series)
        self.assertNotEqual(video.subtitles, None)
        self.assertNotEqual(series.thumbnail, "")
        #self.assertEqual(os.path.isfile("/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S05E19.HDTV.x264-LOL_ov.vtt"), True)
        os.remove("/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S05E19.HDTV.x264-LOL_ov.vtt")

    def test_update_db(self):
        self.assertEqual(Series.objects.count(), 0)
        self.assertEqual(Movie.objects.count(), 0)
        #call_command('updatedb')
        update_db_from_local_folder("/usr/src/app/Videos/folder1/", settings.VIDEO_URL)
        self.assertEqual(Series.objects.count(), 1)
        self.assertEqual(Movie.objects.count(), 1)
        shutil.copyfile("/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S05E19.HDTV.x264-LOL.mp4",
                            "/usr/src/app/Videos/folder1/Malcolm.in.the Middle.S03E14.Cynthia's.Back.mp4")
        #call_command('updatedb')
        update_db_from_local_folder("/usr/src/app/Videos/folder1/", settings.VIDEO_URL)
        self.assertEqual(Series.objects.count(), 2)
        self.assertEqual(Movie.objects.count(), 1)
        os.remove("/usr/src/app/Videos/folder1/Malcolm.in.the Middle.S03E14.Cynthia's.Back.mp4")
        #call_command('updatedb')
        update_db_from_local_folder("/usr/src/app/Videos/folder1/", settings.VIDEO_URL)
        self.assertEqual(Series.objects.count(), 1)
        self.assertEqual(Movie.objects.count(), 1)