
import os
import json

def read_credentials():
    with open(os.path.expanduser('~/.deepserve')) as f:
        data = json.load(f)

    return data['api_key']
