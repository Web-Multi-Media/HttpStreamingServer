from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.conf import settings
from django.test import Client, TestCase
import shutil
from django.core.cache import cache
from django.urls import reverse
import json


class UpdateMonitoringTest(TestCase):
    fixtures = ['Videos.json']

    def setUp(self):
        # Every test needs a client.
        self.user = User.objects.create_user(
            username='test_user', password='top_secret')
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client = Client(HTTP_AUTHORIZATION='Token ' + str(self.token))
        self.client.defaults['HTTP_AUTHORIZATION'] = "Token " + str(self.token)

    def test1(self):
        cache.set("ingestion_task_/usr/src/torrent/toto.mp4", "encoding video1", timeout=None)
        shutil.copy("/usr/src/app/Videos/progress/progress_video1",
                    "/usr/progress/progress-log.txt")
        cache.set("video_frames", "1204", timeout=None)
        response = self.client.get(
            reverse('updatedb'),
        )
        #print(response)
        self.assertEqual(response.status_code, 200)
        decoded_content = json.loads(str(response.content, encoding='utf8'))
        print(decoded_content)
        self.assertEqual(decoded_content["toto.mp4"]["percentage"], 0.5016611295681063)

    def test2(self):
        cache.set("ingestion_task_/usr/src/torrent/toto.mp4", "encoding audio", timeout=None)
        shutil.copy("/usr/src/app/Videos/progress/progress_audio1",
                    "/usr/progress/progress-log.txt")
        cache.set("audio_total_duration", "1204", timeout=None)
        response = self.client.get(
            reverse('updatedb'),
        )
        #print(response)
        self.assertEqual(response.status_code, 200)
        decoded_content = json.loads(str(response.content, encoding='utf8'))
        #print(decoded_content["percentage"])
        print(decoded_content)
        self.assertEqual(decoded_content["toto.mp4"]["percentage"], 0.03156146179401993)
