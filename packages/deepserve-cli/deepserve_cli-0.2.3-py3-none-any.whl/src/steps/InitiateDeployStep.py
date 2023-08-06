from ..helpers.colorprint import *

class InitiateDeployStep(object):

    def __init__(self, graphql):
        self.graphql = graphql

    def call(self, version):
        boldp('Deploying model to Deepserve Cloud...', n=1)
        version = self.graphql.cliInitiateVersionDeploy(variables={'versionId': version['id']})

        keyvaluep('Framework: ', version['engine']['libraryString'], 'cyan', t=1, n=1)
        defaultp('Model:     ', t=1)
        cyanp(f'{version["engine"]["inputType"]} ')
        cyanp(version['engine']['outputType'], n=1)

        return version
