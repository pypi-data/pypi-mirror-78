import requests
import sys
import json

from ..helpers.localstorage import read_credentials
from ..helpers.colorprint import *

BASE_URL = 'http://localhost:3000/api/v1/cli'


class APIInterface(object):
    """Interface"""

    def __init__(self, api_key, project_name=None):
        self.api_key        = api_key or read_credentials()
        self.project_name   = project_name
        self.headers        = {"Authorization": ("Bearer %s" % self.api_key),  'DEEPSERVE_PROJECT_NAME': project_name}



    def post(self, route):
        return self.execute('post', route)

    def put(self, route):
        return self.execute('put', route)

    def get(self, route):
        return self.execute('get', route)

    def execute(self, method, route):
        http_methods = {
            'post': self._post,
            'put': self._put,
            'get': self._get,
            }

        try:
            request = http_methods[method](route)

            if request.status_code == 200:
                return { 'status': 'success', 'response': request.json() }
            elif request.status_code == 304:
                return { 'status': 'no_update' }
            elif request.status_code == 404:
                return { 'status': 'not_found' }
            elif request.status_code == 401:
                return { 'status': 'unauthorized' }

            else:
                return {'status': 'failed', 'error': {'request': request }}

        except (requests.exceptions.ConnectionError) as err:
            redp(f'Connection refused. Are you connected to the internet?')
            br()
            return {'status': 'failed', 'error': 'disconnected'}

        except:
            err = sys.exc_info()[0]
            redp("Unexpected error:", sys.exc_info()[0])
            br()
            return {'status': 'failed', 'error': err}


    def _post(self, route):
        return requests.post(f'{BASE_URL}/{route}', headers=self.headers)

    def _put(self, route):
        return requests.put(f'{BASE_URL}/{route}', headers=self.headers)

    def _get(self, route):
        return requests.get(f'{BASE_URL}/{route}', headers=self.headers)
