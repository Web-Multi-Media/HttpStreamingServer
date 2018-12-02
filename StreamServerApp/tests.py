from django.urls import reverse
from django.core.management import call_command
from django.test import Client, TestCase
from StreamServerApp.utils import get_DB_size


class CommandsTestCase(TestCase):
    def test_database_populate_command(self):
        " Test database creation."

        args = []
        opts = {}
        call_command('populatedb', *args, **opts)
        self.assertEqual(get_DB_size(), 3)

class LoadingTest(TestCase):
    fixtures = ['StreamServerApp/fixtures/Videos.json']
    def setUp(self):
            # Every test needs a client.
            self.client = Client()

    def test_load_first_video(self):
        # Issue a GET request.
        response = self.client.get('/StreamServerApp/rendervideo/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_load_home(self):
        # Issue a GET request.
        response = self.client.get('/StreamServerApp/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_search_video_without_query(self):
        response = self.client.get(reverse('search-video'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [])

    def test_search_video_with_query(self):
        expected_result = [{
            'name': 'canard',
            'baseurl': "http://localhost:8000/static/test/test1.mp4",
            'id': 1
        }]
        data = {
            'q': 'cana'
        }
        response = self.client.get(reverse('search-video'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_result)
