from ..interfaces.GraphQLInterface import GraphQLInterface
from ..helpers.colorprint import *
from tabulate import tabulate

def projects(auth_token=None):
    """ProjectsCommand deploy func"""
    return ProjectsCommand(auth_token).call()


class ProjectsCommand(object):
    """ProjectsCommand"""

    def __init__(self, api_key=None):
        self.api_key   = api_key
        self.graphql        = GraphQLInterface(api_key)


    def call(self):
        """ProjectsCommand.call."""
        projects = self.graphql.cliProjects()
        # print('projects', projects)
        br()
        # [self.print_project(p) for p in projects]
        table = [[p['permalink'], p['statusString'], (p['currentVersion'] and p['currentVersion']['nickname']), (p['currentVersion'] and p['currentVersion']['versionAtIdentifierString'])] for p in projects]
        print(tabulate(table, headers=['Project', 'Status', 'Current Version', 'Deployed On']))

        br()

    def print_project(self, project):
        cyanp(f'{project["name"]}', t=1, n=1)
