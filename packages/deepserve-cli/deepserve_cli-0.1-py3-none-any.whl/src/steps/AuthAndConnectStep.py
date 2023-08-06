from ..helpers.colorprint import *
from ..interfaces.GraphQLInterface import GraphQLInterface

class AuthAndConnectStep(object):

    def __init__(self, graphql):
        self.graphql = graphql

    def call(self, project_name):
        boldp('\nConnecting to Deepserve.ai...')
        user = self.graphql.authenticateCli(variables={'projectName': project_name})

        if not user:
            yellowp('\nInvalid credentials. Use `deepserve auth` to authenticate', n=1)
            exit()
        else:
            greenp('done.', n=2)
            keyvaluep('Hi ', user['username'], 'cyan', t=1, n=1)
            keyvaluep('Using project ', project_name, 'cyan', t=1, n=2)

        return user
