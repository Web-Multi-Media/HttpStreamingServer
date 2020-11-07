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

    def _create_test_file(self, path):
        f = open(path, 'w')
        f.write('test123\n')
        f.close()
        f = open(path, 'rb')
        return {'datafile': f}

    def test_upload_file(self):
        url = reverse('subtitles-list')
        data = self._create_test_file('/tmp/test_upload')
        video = Video.objects.create()
        data['video_id'] = video.id
        print(data)


        response = self.client.post(url, data, format='multipart')
        print(response)
