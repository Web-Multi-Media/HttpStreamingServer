import json
import os
import pathlib
import shutil
from os.path import isfile

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from StreamServerApp.database_utils import (get_num_videos)
from StreamServerApp.media_processing import (get_video_type_and_info)
from StreamServerApp.media_management.fileinfo import (createfileinfo,
                                                       readfileinfo)
from StreamServerApp.media_processing import (extract_subtitle,
                                              generate_thumbnail, extract_audio)
from StreamServerApp.models import (Movie, Series, Subtitle, UserVideoHistory,
                                    Video)
from StreamServerApp.subtitles import get_subtitles
from StreamServerApp.tasks import get_subtitles_async, sync_subtitles
from unittest.mock import patch
import shutil

path_to_srt = os.path.join(
    settings.VIDEO_ROOT,
    "Friends S01E07 The One with the Blackout.en.srt")

path_to_vtt = os.path.join(
    settings.VIDEO_ROOT,
    "Friends S01E07 The One with the Blackout.en.vtt")


def mocked_subliminal_download(video, video_path, languages_to_retrieve):

    dict_srt = {}
    dict_vtt = {}
    if "/usr/torrent/" in video_path:
        dict_srt["eng"] = "/usr/torrent/testsub/Friends S01E07 The One with the Blackout.en.srt"
        dict_vtt["eng"] = "/usr/torrent/testsub/Friends S01E07 The One with the Blackout.en.vtt"
    else:
        dict_srt["eng"] = path_to_srt
        dict_vtt["eng"] = path_to_vtt

    return dict_vtt, dict_srt


def resync_test_template(test_instance, input_folder, root_url):
    data = {}
    fake_url = os.path.join(root_url, "folder2/spongebob2.mp4")
    test_folder = "{}/testresync/".format(input_folder)
    try: 
        os.mkdir(test_folder)
    except:
        print("{} exist".format(test_folder))

    extract_audio("/usr/src/app/Videos/folder2/spongebob2.mp4",
                  "{}/testresync/spongebob2.m4a".format(input_folder)
                  )

    video = Video.objects.create(
        name="spongebob2",
        video_url=fake_url,
        video_folder="{}/folder2/spongebob2/playlist.mpd".format(input_folder),
        audio_path="{}/testresync/spongebob2.m4a".format(input_folder))

    subtitle = Subtitle.objects.create(
        srt_path=os.path.join(input_folder,
                              "subtitles/spongebob.srt"),
        video_id=video,
        vtt_path=os.path.join(input_folder,
                              "subtitles/spongebob.vtt"))

    sync_subtitles(subtitle.id)
    subtitle.refresh_from_db()
    expected_url = os.path.join(root_url,
                                "subtitles/spongebob_sync.vtt")
    test_instance.assertEqual(subtitle.webvtt_sync_url, expected_url)


class SubtitlesTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user',
                                             password='top_secret')
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client.defaults['HTTP_AUTHORIZATION'] = str(self.token)

    def test_subtitles_download(self):
        shutil.copy(os.path.join(
            settings.VIDEO_ROOT, "subtitles/test.srt"), path_to_srt)
        shutil.copy(os.path.join(
            settings.VIDEO_ROOT, "subtitles/test.srt"), path_to_vtt)

        subtitles = get_subtitles(
            "/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S05E19.HDTV.x264-LOL.mp4")


        self.assertEqual(
            os.path.isfile(
                path_to_srt
            ), True)
        self.assertEqual(
            os.path.isfile(path_to_vtt, True))

    def test_get_empty_history(self):
        response = self.client.get(reverse('subtitles-list'))
        self.assertEqual(response.status_code, 200)

        results = json.loads(str(response.content, encoding='utf8'))
        #print(results)
        self.assertEqual(results['results'], [])

    def test_subtitle_deleted_when_video_deleted(self):
        video = Video.objects.create()

        subtitle = Subtitle.objects.create(
            srt_path=os.path.join(settings.VIDEO_ROOT,
                                  "subtitles/spongebob.srt"),
            video_id=video,
            vtt_path=os.path.join(settings.VIDEO_ROOT,
                                  "subtitles/spongebob.vtt"))
        video.delete()
        result = Subtitle.objects.filter(pk=subtitle.pk).exists()
        self.assertFalse(result)

    def test_upload_file(self):
        url = reverse('subtitles-list')
        data = {}
        video = Video.objects.create()
        data['video_id'] = video.id
        data['language'] = 'eng'
        data['datafile'] = open('/usr/src/app/Videos/subtitles/test.srt', 'rb')

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201)
        sub = video.subtitles.all()[0]
        expected_url = os.path.join(settings.VIDEO_URL, "test.vtt")
        self.assertEqual(sub.webvtt_subtitle_url, expected_url)

    def test_upload_unicode_file(self):
        url = reverse('subtitles-list')
        data = {}
        video = Video.objects.create()
        data['video_id'] = video.id
        data['language'] = 'fra'
        data['datafile'] = open('/usr/src/app/Videos/subtitles/unicode_fr.srt',
                                'rb')

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201)
        sub = video.subtitles.all()[0]
        expected_url = os.path.join(settings.VIDEO_URL, "unicode_fr.vtt")
        self.assertEqual(sub.webvtt_subtitle_url, expected_url)

    def test_resync_subtitle_in_video_folder(self):
        resync_test_template(self, "/usr/src/app/Videos", "/Videos")

    def test_resync_subtitle_in_torrent_folder(self):
        try:
            os.mkdir("/usr/torrent/subtitles/")
        except:
            print("torrent subtitle folder already exists")
        shutil.copyfile("/usr/src/app/Videos/subtitles/spongebob.srt", "/usr/torrent/subtitles/spongebob.srt")
        resync_test_template(self, "/usr/torrent/", "/torrents")

    @patch('StreamServerApp.subtitles.handle_subliminal_download', side_effect=mocked_subliminal_download)
    def test_subtitles_download(self, mocked):
        shutil.copy("/usr/src/app/Videos/subtitles/spongebob.srt", path_to_srt)
        shutil.copy("/usr/src/app/Videos/subtitles/spongebob.srt", path_to_vtt)
        subtitles = get_subtitles(
            "/usr/src/app/Videos/Friends S01E07 The One with the Blackout.mp4")
        self.assertEqual(
            os.path.isfile(path_to_srt
                           ), True)
        self.assertEqual(
            os.path.isfile(path_to_vtt
                           ), True)

    @patch('StreamServerApp.subtitles.handle_subliminal_download', side_effect=mocked_subliminal_download)
    def test_get_subtitles_async_1(self, mocked):
        expected_url = os.path.join(
            settings.VIDEO_URL,
            "Friends S01E07 The One with the Blackout.en.vtt")

        path_to_dash_asset = "/usr/src/app/Videos/testsub/"
        if not os.path.isdir(path_to_dash_asset):
            #os.mkdir("/usr/test/FriendsS01E07TheOnewiththeBlackout/", exist_ok=True)
            pathlib.Path(path_to_dash_asset).mkdir(parents=True, exist_ok=True)

        video_info = {
            "video_full_path":
            "{}/Friends S01E07 The One with the Blackout.mp4".format(
                path_to_dash_asset)
        }
        createfileinfo("{}/fileinfo.json".format(path_to_dash_asset),
                       video_info)
        video = Video.objects.create(
            name="Man On The Moon.mp4",
            video_folder="{}/playlist.mpd".format(path_to_dash_asset))

        get_subtitles_async(video.id, "/usr/src/app/Videos/", "/Videos/")

        assert (len(video.subtitles.filter(language="eng")) > 0)
        sub = video.subtitles.filter(language="eng")[0]
        self.assertEqual(sub.webvtt_subtitle_url, expected_url)


    @patch('StreamServerApp.subtitles.handle_subliminal_download', side_effect=mocked_subliminal_download)
    def test_get_subtitles_async_2(self , mocked):
        path_to_dash_asset = "/usr/torrent/testsub/"
        if not os.path.isdir(path_to_dash_asset):
            #os.mkdir("/usr/test/FriendsS01E07TheOnewiththeBlackout/", exist_ok=True)
            pathlib.Path(path_to_dash_asset).mkdir(parents=True, exist_ok=True)

        video_info = {
            "video_full_path":
            "{}/Friends S01E07 The One with the Blackout.mp4".format(
                path_to_dash_asset)
        }
        createfileinfo("{}/fileinfo.json".format(path_to_dash_asset),
                       video_info)
        video = Video.objects.create(
            name="Man On The Moon.mp4",
            video_folder="{}/playlist.mpd".format(path_to_dash_asset))

        get_subtitles_async(video.id, "/usr/torrent/", "/torrents/")

        expected_url = os.path.join(
            "/torrents/",
            "testsub/Friends S01E07 The One with the Blackout.en.vtt")

        assert (len(video.subtitles.filter(language="eng")) > 0)
        sub = video.subtitles.filter(language="eng")[0]
        self.assertEqual(sub.webvtt_subtitle_url, expected_url)

