from ..helpers.colorprint import *

class CreateVersionStep(object):

    def __init__(self, graphql):
        self.graphql = graphql

    def call(self, project_name, notebook_path=None):
        boldp('Creating new version...')
        version = self.graphql.cliCreateVersion(variables={'projectPermalink': project_name, 'notebookFilename': notebook_path})

        greenp('done.', n=2)
        keyvaluep('Version: ', version['nickname'], 'cyan', t=1, n=1)
        keyvaluep('Timestamp: ', version['versionAtIdentifierString'], 'cyan', t=1, n=2)

        return version
