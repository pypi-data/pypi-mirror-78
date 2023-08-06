import os
import warnings
from ..helpers.colorprint import *
from ..interfaces.S3Interface import S3Interface

class UploadNotebookStep(object):

    def __init__(self, graphql):
        self.graphql = graphql

    def call(self, version, file_path):
        boldp('Converting jupyter notebook...')
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            os.system(f'jupyter nbconvert --to html {file_path} --log-level 50')
        html_path = f'{os.path.splitext(file_path)[0]}.html'

        S3Interface().direct_upload_file(html_path, version['presignedS3NotebookUploadUrl'], version['presignedS3NotebookUploadKey'])
        greenp('done.', n=2)
        os.remove(html_path)
