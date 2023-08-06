from ..helpers.colorprint import *
from ..interfaces.S3Interface import S3Interface

class UploadModelStep(object):

    def __init__(self, graphql):
        self.graphql = graphql

    def call(self, version, file_path):
        boldp('Uploading model...')
        S3Interface().direct_upload_file(file_path, version['presignedS3UploadUrl'], version['presignedS3UploadKey'])
        greenp('done.', n=2)
