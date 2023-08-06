
import json
import requests as res
from requests import Response
from .exceptions import TokenError


class Token:

    def __init__(self, path: str, username: str, password: str):
        self.path = path
        self.username = username
        self.password = password
        request_token = self.request_token()

        if json.loads(request_token.text)['result'] == 'success':
            self.request_token = request_token.text
        else:
            raise TokenError

    def __repr__(self):
        return self.request_token

    def request_token(self) -> Response:
        return res.post(self.path + 'tokens', json={"grant_type": "password", "username": self.username,
                                                    "password": self.password})

    def get_token(self):
        return json.loads(self.request_token)['token']
