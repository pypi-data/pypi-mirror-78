import copy
import logging

import flask
import requests

from avatar_utils.tests.AbstractApp import AbstractApp
from avatar_utils.tests.Env import *

logger = logging.getLogger(__name__)


class RemoteApp(AbstractApp):
    client = requests

    # default env, specified once per whole test class
    default_env = DevEnv()

    # current env, could be changed in every test fuction
    current_env = copy.deepcopy(default_env)

    @property
    def base_url(self):
        return self.current_env.base_url

    def post(self, url, data=dict()) -> flask.Response:
        res = super().post(self.base_url + url, data)
        return self.convert_to_flask_response(res)

    def get(self, url, data=dict()) -> flask.Response:
        res = super().get(self.base_url + url, data)
        return self.convert_to_flask_response(res)

    # TODO transfer headers
    @staticmethod
    def convert_to_flask_response(response: requests.Response) -> flask.Response:
        res = flask.Response(
            response=response.text,
            status=response.status_code,
            mimetype=response.headers['content-type']
        )

        return res
