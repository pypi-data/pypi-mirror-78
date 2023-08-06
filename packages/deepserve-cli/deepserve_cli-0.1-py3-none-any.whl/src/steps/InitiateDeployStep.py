from ..helpers.colorprint import *

class InitiateDeployStep(object):

    def __init__(self, graphql):
        self.graphql = graphql

    def call(self, version):
        boldp('Deploying model to Deepserve Cloud...', n=1)
        version = self.graphql.cliInitiateVersionDeploy(variables={'versionId': version['id']})

        keyvaluep('Language:  ', version['engine']['languageString'], 'cyan', t=1, n=1)
        keyvaluep('Framework: ', version['engine']['libraryString'], 'cyan', t=1, n=1)
        keyvaluep('Input:     ', version['pattern']['inputStrategy'], 'cyan', t=1, n=1)
        keyvaluep('Output:    ', version['pattern']['outputStrategy'], 'cyan', t=1, n=2)


        return version
