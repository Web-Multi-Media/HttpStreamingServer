
from django.core.management import call_command
from django.test import Client, TestCase


class CommandsTestCase(TestCase):
    def test_mycommand(self):
        " Test my custom command."

        args = []
        opts = {}
        call_command('populatedb', *args, **opts)

class LoadingTest(TestCase):
    def setUp(self):
            # Every test needs a client.
            self.client = Client()

    def test_load_home(self):
        # Issue a GET request.
        response = self.client.get('/StreamServerApp/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

