import requests
import sys
import json
from ..helpers.colorprint import *
from ..helpers.error_boundary import HTTPErrorBoundary

class S3Interface(object):
    """S3Interface"""

    def direct_upload_file(self, file_path, upload_url, object_key):
        with HTTPErrorBoundary():
            with open(file_path, 'rb') as f:
                # files = {'file': (object_key, f)}
                request = requests.put(upload_url, data=open(file_path, 'rb'))
                # request = requests.put(upload_url, files=files)
                if request.status_code == 200:
                    return True
                else:
                    redp('\nFailed to upload.', n=1)
                    exit()
