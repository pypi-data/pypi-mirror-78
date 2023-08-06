
# https://stackoverflow.com/questions/13909900/progress-of-python-requests-post
# https://pypi.org/project/progressbar2/
# https://pypi.org/project/progress/
# https://pypi.org/project/tqdm/



import os
import requests
from .colorprint import *
import urllib
import mmap
import logging
import websocket
import time
# from tqdm import tqdm
from halo import Halo
try:
    import thread
except ImportError:
    import _thread as thread
import time
import pysher

from .APIInterface import APIInterface
from .S3Interface import S3Interface



def deploy(project_name, file_path, auth_token):
    """DeployCommand deploy func"""
    return DeployCommand(project_name, file_path, auth_token).call()


class DeployCommand(object):
    """DeployCommand"""

    def __init__(self, project_name, file_path, api_key=None):
        self.project_name   = project_name
        self.file_path      = file_path
        self.api            = APIInterface(api_key, project_name)

    def call(self):
        """DeployCommand.call."""

        br()
        boldp('Connecting to Deepserve.ai...')
        if not self.auth_and_connect():
            return None

        greenp('done.')
        br(2)
        defaultp('Hi ', tabs=1) and cyanp(self.username)
        br()
        defaultp('Using project ', tabs=1) and cyanp(self.project_name)
        br(2)

        boldp('Creating new version...')
        greenp('done.')
        br(2)

        defaultp('Version: ', tabs=1) and cyanp(self.version_nickname)
        br()
        defaultp('Timestamp: ', tabs=1) and cyanp(self.version_at_string)
        br(2)

        boldp('Uploading model...')
        if not self.upload_file():
            redp('\nFailed to upload model.')
            return None
        greenp('done.')
        br(2)

        deploy_status = self.deploy_model()
        if not deploy_status:
            redp('Failed to deploy engine.')
            return None
        if deploy_status == 'no_update':
            yellowp('Model already up to date.')
            return None


        br(2)
        boldp('Deploying engine...')
        br()
        defaultp('Language:   ', tabs=1) and cyanp(self.language_string)
        br()
        defaultp('Framework:  ', tabs=1) and cyanp(self.library_string)
        br()
        defaultp('Input:      ', tabs=1) and cyanp(self.input)
        br()
        defaultp('Output:     ', tabs=1) and cyanp(self.output)
        br()

        monitor_deploy = self.monitor_status()


        if (monitor_deploy == 'active'):
            greenp('Done.')
            br(2)
            defaultp(f'Congrats! {self.project_name} is now available')
            br()
            defaultp(f'Endpoint: ') and greenp(f'https://deepserve-api.com/{self.project_permalink}')
            br(4)

        elif monitor_deploy == 'deploy_failed':
            redp('Deploy failed.')
            br(4)
            return None

    def auth_and_connect(self):
        response = self.api.post('versions')

        if response['status'] == 'success':
            self.version_id = response['response']['version_id']
            self.s3_upload_url = response['response']['upload_url']
            self.s3_object_key = response['response']['object_key']
            self.version_nickname = response['response']['version']['nickname']
            self.project_name = response['response']['project']['name']
            self.project_permalink = response['response']['project']['permalink']
            self.version_at_string = response['response']['version']['version_at_string']
            self.username = response['response']['project']['username']
            return True
        elif response['status'] == 'unauthorized':
            redp('Authentication invalid. Run `deepserve auth` to re-authenticate')
            return False
        elif response['status'] == 'not_found':
            redp('Project `%s` not found' % self.project_name)
            return False
        else:
            redp('Failed to connect to Deepserve.ai.')
            return False
            # return response['error']


    def upload_file(self):
        response = S3Interface().direct_upload_file(self.file_path, self.s3_upload_url, self.s3_object_key)
        return response['status'] == 'success'

    def deploy_model(self):
        response = self.api.put(f'versions/{self.version_id}/deploy')
        if response['status'] == 'success':
            self.version_nickname = response['response']['version']['nickname']
            self.username = response['response']['project']['username']
            self.library_string = response['response']['engine']['library_string']
            self.language_string = response['response']['engine']['language']
            self.input = response['response']['pattern']['input']
            self.output = response['response']['pattern']['output']
            return True
        elif response['status'] == 'no_update':
            return 'no_update'
        else:
            return False

    def monitor_status(self):
        deploy_status = 'deploying'
        with Halo(text='This may take a few minutes', spinner='dots'):
            while deploy_status == 'deploying':
                response = self.api.get(f'versions/{self.version_id}')
                if response['status'] == 'success':
                    deploy_status = response['response']['version']['status']
                    time.sleep(1)
                else:
                    redp('\nSomething went wrong')
                    return False

        return deploy_status
