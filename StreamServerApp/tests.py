from django.test import TestCase


import unittest
from django.test import Client

class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_home(self):
        # Issue a GET request.
        response = self.client.get('/StreamServerApp/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)