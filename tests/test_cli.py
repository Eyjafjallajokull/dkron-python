import unittest
import json
import os
import requests_mock as rmock
from dkron_cli.api import DkronApi


class DkronApiTestCase(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://localhost'
        self.api = DkronApi(self.base_url)

    def get_url(self, url):
        return self.base_url + url

    def test_get_jobs(self):
        expected = {'foo': 'bar'}
        with rmock.Mocker() as mocker:
            mocker.register_uri(
                rmock.GET,
                self.get_url('/v1/jobs'),
                text=json.dumps(expected),
                status_code=200
            )
            results = self.api.get_jobs()
            self.assertEquals(results, expected)
