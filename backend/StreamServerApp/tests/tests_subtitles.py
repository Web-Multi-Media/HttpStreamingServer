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

from django.conf import settings
from StreamServerApp.tasks import sync_subtitles




class SubtitlesTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test_user', password='top_secret')
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client.defaults['HTTP_AUTHORIZATION'] = str(self.token)

    def test_get_empty_history(self):
        response = self.client.get(reverse('subtitles-list'))
        self.assertEqual(response.status_code, 200)

        results = json.loads(str(response.content, encoding='utf8'))
        #print(results)
        self.assertEqual(results['results'], [])

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
        self.assertEqual(sub.webvtt_subtitle_url, "/Videos/test.vtt")


    def test_upload_unicode_file(self):
        url = reverse('subtitles-list')
        data = {}
        video = Video.objects.create()
        data['video_id'] = video.id
        data['language'] = 'fra'
        data['datafile'] = open('/usr/src/app/Videos/subtitles/unicode_fr.srt', 'rb')

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201)
        sub = video.subtitles.all()[0]
        self.assertEqual(sub.webvtt_subtitle_url, "/Videos/unicode_fr.vtt")

    def test_resync_subtitle(self):

        data = {}
        video = Video.objects.create(name="spongebob.mp4",
                                     video_url=os.path.join(settings.VIDEO_URL, "folder2/spongebob.mp4"))
        video.save()                      

        subtitle = Subtitle.objects.create(srt_path=os.path.join(settings.VIDEO_ROOT, "subtitles/spongebob.srt"),
        video_id = video, vtt_path=os.path.join(settings.VIDEO_ROOT, "subtitles/spongebob.vtt"))
        subtitle.save()

        sync_subtitles(video.id, subtitle.id)
        #print("URL" + subtitle.webvtt_sync_url + "coucou")
        self.assertEqual(subtitle.webvtt_sync_url, "/Videos/subtitles/spongebob_sync.vtt")

