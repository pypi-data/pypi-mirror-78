import requests
from requests.auth import HTTPBasicAuth

from .Config import Config

class UserAgent:
    def __init__(self):
        config = Config()
        config_ref = config.get_config()
        self.auth = HTTPBasicAuth(config_ref['user'], config_ref['password'])

    def get(self, endpoint):
        response = requests.get(endpoint, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data={}):
        response = requests.post(endpoint, auth=self.auth, json=data)
        response.raise_for_status()
        return response.json()
