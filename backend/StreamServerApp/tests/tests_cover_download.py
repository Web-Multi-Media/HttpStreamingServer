from django.test import TestCase
import os
from unittest import TestCase, mock
from StreamServerApp.media_management.cover_downloader import cover_downloader
import optparse

class CoverDownloaderTest(TestCase):

    def setUp(self):
        pass

    @mock.patch.dict(os.environ, {"TMBD_KEY": ""})
    def test_ensureErrorWithInvalidToken(self):

        cvdwnld = cover_downloader()
        self.assertEqual(cvdwnld.download_cover("test", "/test/test.jpeg", True), -1)

