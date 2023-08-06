from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import requests

from ..helpers.localstorage import read_credentials
from ..helpers.colorprint import *
from ..helpers.error_boundary import HTTPErrorBoundary

GRAPHQL_ENDPOINT = 'http://localhost:3000/graphql'

class GraphQLInterface(object):
    """Interface"""

    def __init__(self, api_key=None):
        self.api_key = api_key or read_credentials()
        self.client = None

        with HTTPErrorBoundary():
            self.client = Client(
                transport=RequestsHTTPTransport(
                    url=GRAPHQL_ENDPOINT,
                    use_json=True,
                    headers={
                        "Content-type": "application/json",
                        "Authorization": ("Bearer %s" % self.api_key)
                    },
                    verify=False,
                    retries=3,
                ),
                fetch_schema_from_transport=True,
            )


    def execute(self, query, variables, key=None):
        with HTTPErrorBoundary():
            # query = getattr(self, query_name)()
            res = self.client.execute(query, variable_values=variables)
            if not res:
                raise requests.exceptions.HTTPError
            return res



    def authenticateCli(self, variables={}):
        query = gql('''
            query AuthenticateCli {
                currentUser {
                    username
                }
            }
        ''')

        res = self.execute(query, {'input': variables})
        return res['currentUser']


    def versionStatus(self, variables={}):
        query = gql('''
            query VersionStatus($versionId: ID!) {
                version(versionId: $versionId) {
                    status
                    statusString
                }
            }
        ''')

        res = self.execute(query, variables)
        return res['version']['status']

    def cliProjects(self, variables={}):
        query = gql('''
            query CliProjects {
                cliProjects {
                    id
                    name
                    username
                    permalink
                    statusString
                    currentVersion {
                        id
                        nickname
                        statusString
                        versionAtIdentifierString
                    }
                }
            }
        ''')

        res = self.execute(query, variables)
        return res['cliProjects']


    def cliCreateVersion(self, variables={}):
        query = gql('''
            mutation CLICreateVersion($input: CreateVersionInput!) {
                cliCreateVersion(input: $input) {
                    version {
                        id
                        nickname
                        versionAtIdentifierString
                        presignedS3UploadUrl
                        presignedS3UploadKey
                        presignedS3NotebookUploadUrl
                        presignedS3NotebookUploadKey
                        pattern {
                            inputStrategy
                            outputStrategy
                        }
                        engine {
                            libraryString
                            languageString
                        }
                    }
                }
            }
        ''')

        res = self.execute(query, {'input': variables})
        return res['cliCreateVersion']['version']

    def cliInitiateVersionDeploy(self, variables={}):
        query = gql('''
            mutation CliInitiateVersionDeploy($input: InitiateVersionDeployInput!) {
                cliInitiateVersionDeploy(input: $input) {
                    version {
                        id
                        nickname
                        versionAtIdentifierString
                        project {
                            permalink
                        }
                        pattern {
                            inputStrategy
                            outputStrategy
                        }
                        engine {
                            libraryString
                            languageString
                        }
                    }
                }
            }
        ''')

        res = self.execute(query, {'input': variables})
        return res['cliInitiateVersionDeploy']['version']
