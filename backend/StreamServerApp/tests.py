from django.urls import reverse
from django.core.management import call_command
from django.test import Client, TestCase
from StreamServerApp.utils import get_DB_size, get_video_type_and_info


class CommandsTestCase(TestCase):
    def test_database_populate_command(self):
        " Test database creation."

        args = []
        opts = {}
        call_command('populatedb', *args, **opts)
        self.assertEqual(get_DB_size(), 5)


class LoadingTest(TestCase):
    fixtures = ['Videos.json']
    def setUp(self):
            # Every test needs a client.
            self.client = Client()

    def test_search_video_without_query(self):
        response = self.client.get(reverse('videos-list'))
        self.assertEqual(response.status_code, 200)
        #self.assertJSONEqual(str(response.content, encoding='utf8'), [])

    def test_search_video_with_query(self):
        data = {
            'search_query': 'The.Big.Bang.Theory.S05E19.HDTV.x264-LOL.mp4'
        }
        response = self.client.get(reverse('videos-list'), data=data)
        self.assertEqual(response.status_code, 200)
        #self.assertJSONEqual(str(response.content, encoding='utf8'), expected_result)


class UtilsTest(TestCase):
    def test_movie_series_info_parsing(self):
        series_name = 'The.Big.Bang.Theory.S05E19.HDTV.x264-LOL.mp4'
        movie_name = 'The Blues Brothers (1980) [1080p]/The.Blues.Brothers.1980.1080p.BrRip.x264.bitloks.YIFY.jpg'
        series_info = get_video_type_and_info(series_name)
        movie_info = get_video_type_and_info(movie_name)

        self.assertEqual(series_info['type'], 'Series')
        self.assertEqual(series_info['title'], 'The Big Bang Theory')
        self.assertEqual(series_info['season'], 5)
        self.assertEqual(series_info['episode'], 19)

        self.assertEqual(movie_info['type'], 'Movie')
        self.assertEqual(movie_info['title'], 'The Blues Brothers')
