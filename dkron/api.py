import requests
import os


class DkronException(Exception):
    pass


class Dkron():
    def __init__(self, dkron_api_url):
        self.base_url = dkron_api_url
        self.raise_errors = True

    def _get_url(self, path):
        return self.base_url + path

    def _get_headers(self):
        return {}

    def _process_response(self, response):
        if self.raise_errors and response.status_code not in [200, 201, 202]:
            raise DkronApiException('Dkron API request failed with code %d, %s' %
                (response.status_code, response.text))
        return response.json()

    def get_status(self):
        url = self._get_url('/v1')
        response = requests.get(url, headers=self._get_headers())
        return self._process_response(response)

    def get_leader(self):
        url = self._get_url('/v1/leader')
        response = requests.get(url, headers=self._get_headers())
        return self._process_response(response)

    def get_members(self):
        url = self._get_url('/v1/members')
        response = requests.get(url, headers=self._get_headers())
        return self._process_response(response)

    def get_jobs(self):
        url = self._get_url('/v1/jobs')
        response = requests.get(url, headers=self._get_headers())
        return self._process_response(response)

    def get_job(self, name):
        url = self._get_url('/v1/jobs/%s' % name)
        response = requests.get(url, headers=self._get_headers())
        return self._process_response(response)

    def apply_job(self, data):
        url = self._get_url('/v1/jobs')
        response = requests.post(url, headers=self._get_headers(), json=data)
        return self._process_response(response)

    def run_job(self, name):
        url = self._get_url('/v1/jobs/%s' % name)
        response = requests.post(url, headers=self._get_headers())
        return self._process_response(response)

    def delete_job(self, name):
        url = self._get_url('/v1/jobs/%s' % name)
        response = requests.delete(url, headers=self._get_headers())
        return self._process_response(response)

    def get_executions(self, job_name):
        url = self._get_url('/v1/executions/%s' % job_name)
        response = requests.get(url, headers=self._get_headers())
        return self._process_response(response)
