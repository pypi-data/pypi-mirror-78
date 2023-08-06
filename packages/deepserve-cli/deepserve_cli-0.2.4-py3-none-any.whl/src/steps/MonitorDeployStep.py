from ..helpers.colorprint import *
from halo import Halo
try:
    import thread
except ImportError:
    import _thread as thread

import time

class MonitorDeployStep(object):

    def __init__(self, graphql):
        self.graphql = graphql

    def call(self, version):
        try:
            status = 'deploying'
            with Halo(text='This may take a few minutes', spinner='dots'):
                while status == 'deploying':
                    status = self.graphql.versionStatus(variables={'versionId': version['id']})
                    time.sleep(5)


            if status == 'active':
                greenp('Done.', n=2)
                defaultp(f'Congrats! Version {version["nickname"]} of {version["project"]["permalink"]} is now available', n=1)
                defaultp(f'Endpoint: ')
                greenp(f'https://deepserve-api.com/{version["project"]["permalink"]}', n=3)
            else:
                redp('\nThe deploy failed.')
                exit()
        except KeyboardInterrupt:
            yellowp('\nExited. The deploy is still underway.', n=2)
            # defaultp('To cancel the deploy, run: ', n=1)
            # cyanp(f'deepserve cancel {version["project"]["permalink"]}', t=1, n=2)
            # defaultp('To monitor the status, run: ', n=1)
            # cyanp(f'deepserve status {version["project"]["permalink"]}', t=1, n=2)
            # exit()
