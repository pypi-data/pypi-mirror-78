import os
import json


def auth():
    """Connect your API token to Deepserve"""
    api_key = input('Enter your API key: ')
    creds = {'api_key': api_key}

    with open(os.path.expanduser('~/.deepserve'), 'w') as f:
        json.dump(creds, f)

    print("Credentials saved to ~/.deepserve\n")
