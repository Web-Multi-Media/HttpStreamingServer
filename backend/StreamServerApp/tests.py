import os
import json
from os.path import isfile
from django.urls import reverse
from django.core.management import call_command
from django.test import Client, TestCase
from django.conf import settings
from StreamServerApp.utils import get_num_videos, get_video_type_and_info
from StreamServerApp.models import Video, Series, Movie
from StreamServerApp.media_processing import extract_subtitle, generate_thumbnail
from StreamServerApp.subtitles import get_subtitles


class CommandsTestCase(TestCase):
    def test_database_populate_command(self):
        " Test database creation."

        args = []
        opts = {}
        call_command('populatedb', *args, **opts)
        # a bit of a mess here to make sure to count only files in all folders...
        files_in_videos_folders = [[os.path.join(root, file) for file in files] for root, _, files in os.walk(settings.VIDEO_ROOT)]
        video_files = [filename for sublist in files_in_videos_folders for filename in sublist  # flatten nested list
                       if isfile(filename) and (filename.endswith(".mp4") or filename.endswith(".mkv"))]
        self.assertEqual(get_num_videos(), len(video_files))


class LoadingTest(TestCase):
    fixtures = ['Videos.json']
    def setUp(self):
            # Every test needs a client.
            self.client = Client()

    def test_search_video_without_query(self):
        response = self.client.get(reverse('videos-list'))
        self.assertEqual(response.status_code, 200)

        # check that we get all the 3 videos from the Videos.json fixture
        results = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(len(results['results']), 3)

    def test_search_video_with_query(self):
        data = {
            'search_query': 'The Big Bang theory'
        }
        expected_result_name = 'The.Big.Bang.Theory.S05E19.HDTV.x264-LOL.mp4'

        response = self.client.get(reverse('videos-list'), data=data)
        self.assertEqual(response.status_code, 200)
        
        # check that the first result is the best match
        results = json.loads(str(response.content, encoding='utf8'))
        retrieved_name = results['results'][0]['name']  
        self.assertEqual(expected_result_name, retrieved_name)


class UtilsTest(TestCase):
    def test_movie_series_info_parsing(self):
        # We check that the parser gets the correct information from the filenames
        series_name = 'The.Big.Bang.Theory.S05E19.HDTV.x264-LOL.mp4'
        series_name2 = 'The.Big.Bang.Theory.S05E18.HDTV.x264-LOL.mp4'
        series_name3 = 'Futurama S02E10 Put Your Head On My Shoulders.mp4'
        series_name4 = 'Futurama.S01.E10.Fake_name*withçweird&cg!"%&()@.mp4'
        series_name5 = 'Futurama [1x11] Fake_name_2*wasfqwef&cg!"%&()@.mp4'
        series_name6 = '02- Black Mirror[S1E2]Fifteen Million Merits.720p.x264-kmcrct.mp4'
        movie_name = 'The Blues Brothers (1980) [1080p]/The.Blues.Brothers.1980.1080p.BrRip.x264.bitloks.YIFY.jpg'
        series_info = get_video_type_and_info(series_name)
        series_info2 = get_video_type_and_info(series_name2)
        series_info3 = get_video_type_and_info(series_name3)
        series_info4 = get_video_type_and_info(series_name4)
        series_info5 = get_video_type_and_info(series_name5)
        series_info6 = get_video_type_and_info(series_name6)
        movie_info = get_video_type_and_info(movie_name)

        self.assertEqual(series_info['type'], 'Series')
        self.assertEqual(series_info['title'], 'The Big Bang Theory')
        self.assertEqual(series_info['season'], 5)
        self.assertEqual(series_info['episode'], 19)

        self.assertEqual(series_info2['season'], 5)
        self.assertEqual(series_info3['title'], series_info4['title'])
        self.assertEqual(series_info3['season'], 2)
        self.assertEqual(series_info4['season'], 1)
        self.assertEqual(series_info5['season'], 1)
        self.assertEqual(series_info5['episode'], 11)

        self.assertEqual(series_info6['title'], 'Black Mirror')
        self.assertEqual(series_info6['episode'], 2)

        self.assertEqual(movie_info['type'], 'Movie')
        self.assertEqual(movie_info['title'], 'The Blues Brothers')

    def test_movies_series_added_to_db(self):
        # We check that only one Series instance is created (2 bing band theory episodes)
        # and 4 Movie instances are created.
        # We also check that the video fields are set correctly.
        call_command('populatedb')

        self.assertEqual(Series.objects.count(), 1)
        self.assertEqual(Movie.objects.count(), 4)

        video = Video.objects.get(name='The.Big.Bang.Theory.S05E19.HDTV.x264-LOL.mp4')
        series = Series.objects.first()
        self.assertEqual(video.episode, 19)
        self.assertEqual(video.season, 5)
        self.assertEqual(video.series, series)
        self.assertNotEqual(series.thumbnail, "")
        self.assertEqual(os.path.isfile("/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S05E19.HDTV.x264-LOL_ov.vtt"), True)
        os.remove("/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S05E19.HDTV.x264-LOL_ov.vtt")

    def test_subtitles_extraction(self):
        extract_subtitle("/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S05E19.HDTV.x264-LOL.mp4",
                        "/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S05E19.HDTV.x264-LOL_ov.vtt")
        self.assertEqual(os.path.isfile("/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S05E19.HDTV.x264-LOL_ov.vtt"), True)
        os.remove("/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S05E19.HDTV.x264-LOL_ov.vtt")

    def test_subtitles_download(self):
        subtitles = get_subtitles("/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S05E19.HDTV.x264-LOL.mp4", True)
        self.assertEqual(os.path.isfile("/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S05E19.HDTV.x264-LOL.en.vtt"), True)
        self.assertEqual(os.path.isfile("/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S05E19.HDTV.x264-LOL.fr.vtt"), True)
        os.remove("/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S05E19.HDTV.x264-LOL.en.vtt")
        os.remove("/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S05E19.HDTV.x264-LOL.fr.vtt")
        os.remove("/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S05E19.HDTV.x264-LOL_ov.vtt")

    def test_thumbnail_generation(self):
        generate_thumbnail("/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S05E19.HDTV.x264-LOL.mp4", 1.0,
                        "/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S05E19.HDTV.x264-LOL.jpeg")
        self.assertEqual(os.path.isfile("/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S05E19.HDTV.x264-LOL.jpeg"), True)
        os.remove("/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S05E19.HDTV.x264-LOL.jpeg")