import requests
import ast
from .colorprint import *

class HTTPErrorBoundary(object):
    # def __init__(self):
        # self.context = context
    def __enter__(self):
        return self
        # return self.context
    def __exit__(self, type, value, trace_back):

        if type == requests.exceptions.ConnectionError:
            redp('\nConnection refused. Are you connected to the internet?', n=1)
            exit()

        elif type == requests.exceptions.HTTPError:
            redp('\nThe Deepserve API is currently unavailable. Please try again later.', n=1)
            exit()
        elif type:
            print('value', value)
            if value.args[0]:
                error = ast.literal_eval(value.args[0])
                if error and error['extensions']:
                    extensions = error['extensions']
                    if extensions['code'] == 404:
                        yellowp(f'\nWe couldn\'t find what you\'re looking for. Are you sure that\'s the right project?', n=1)
                        exit()
                        return True
            else:
                redp(f'Unexpected error [{type}]: {value}', n=1)
                # redp(f'\nUnexpected error [{type}]: {value}', n=1)
                # exit()
            # if value.args[0] and value.args[0]['extensions'] and value.args[0]['extensions']['code'] == 404:
            #     print('4040404040404040404040404', value)
            #     exit()


        else:
            return True
