from unittest import TestCase
import json
import os
import requests_mock as rmock
from dkron.api import Dkron, DkronException


class DkronTestCase(TestCase):
    def setUp(self):
        self.hosts = ['http://localhost:8080']
        with rmock.Mocker() as mocker:
            self._get_simple_mock(mocker, '/v1', {})
            self.api = Dkron(self.hosts)

    def _get_simple_mock(self, mocker, url, response_data, method=rmock.GET, code=200):
        mocker.register_uri(
            method,
            self.get_url(url),
            text=json.dumps(response_data),
            status_code=code
        )

    def get_url(self, url):
        return self.hosts[0] + url

    def test_host_selection(self):
        hosts = ['http://localhost:8080', 'http://localhost2:8080', 'http://localhost3:8080']
        with rmock.Mocker() as mocker:
            mocker.register_uri(rmock.GET, hosts[0]+'/v1', status_code=500, text="[]")
            mocker.register_uri(rmock.GET, hosts[1]+'/v1', status_code=200, text="[]")
            api = Dkron(hosts)
            self.assertEquals(api.base_url, hosts[1])

    def test_no_host(self):
        hosts = ['http://localhost:8080']
        with rmock.Mocker() as mocker:
            mocker.register_uri(rmock.GET, hosts[0]+'/v1', status_code=500, text="[]")
            with self.assertRaises(DkronException) as context:
                Dkron(hosts)

    def test_status_exception(self):
        with rmock.Mocker() as mocker:
            mocker.register_uri(
                rmock.GET,
                self.get_url('/v1'),
                status_code=404
            )
            with self.assertRaises(DkronException) as context:
                self.api.get_status()

    def test_get_status(self):
        expected = {'foo': 'bar'}
        with rmock.Mocker() as mocker:
            self._get_simple_mock(mocker, '/v1', expected)
            results = self.api.get_status()
            self.assertEquals(results, expected)

    def test_get_leader(self):
        expected = {'foo': 'bar'}
        with rmock.Mocker() as mocker:
            self._get_simple_mock(mocker, '/v1/leader', expected)
            results = self.api.get_leader()
            self.assertEquals(results, expected)

    def test_get_members(self):
        expected = {'foo': 'bar'}
        with rmock.Mocker() as mocker:
            self._get_simple_mock(mocker, '/v1/members', expected)
            results = self.api.get_members()
            self.assertEquals(results, expected)

    def test_get_jobs(self):
        expected = {'foo': 'bar'}
        with rmock.Mocker() as mocker:
            self._get_simple_mock(mocker, '/v1/jobs', expected)
            results = self.api.get_jobs()
            self.assertEquals(results, expected)

    def test_get_job(self):
        expected = {'foo': 'bar'}
        with rmock.Mocker() as mocker:
            self._get_simple_mock(mocker, '/v1/jobs/foo', expected)
            results = self.api.get_job('foo')
            self.assertEquals(results, expected)

    def test_run_job(self):
        expected = {'foo': 'bar'}
        with rmock.Mocker() as mocker:
            self._get_simple_mock(mocker, '/v1/jobs/foo', expected, method=rmock.POST)
            results = self.api.run_job('foo')
            self.assertEquals(results, expected)

    def test_apply_job(self):
        expected = {'foo': 'bar'}
        with rmock.Mocker() as mocker:
            self._get_simple_mock(mocker, '/v1/jobs', expected, method=rmock.POST)
            results = self.api.apply_job({})
            self.assertEquals(results, expected)

    def test_delete_job(self):
        expected = {'foo': 'bar'}
        with rmock.Mocker() as mocker:
            self._get_simple_mock(mocker, '/v1/jobs/foo', expected, method=rmock.DELETE)
            results = self.api.delete_job('foo')
            self.assertEquals(results, expected)

    def test_get_executions(self):
        expected = {'foo': 'bar'}
        with rmock.Mocker() as mocker:
            self._get_simple_mock(mocker, '/v1/executions/foo', expected)
            results = self.api.get_executions('foo')
            self.assertEquals(results, expected)
