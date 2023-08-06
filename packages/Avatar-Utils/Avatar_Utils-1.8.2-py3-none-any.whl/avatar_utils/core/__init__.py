from logging import getLogger
from typing import Dict
from typing import Tuple

import requests
from flask import jsonify
from flask.wrappers import Response

from avatar_utils.objects.abstracts.serializable import Serializable

logger = getLogger(__name__)


class RequestTool:
    def post(self, url, data=dict()):
        headers = {'Content-type': 'application/json'}
        return requests.post(url, json=data, headers=headers)


class ResponseTool:

    def __init__(self, default_headers=dict()):
        self.default_headers = default_headers

    def create(self, data: dict = None, status: int = 200, message: str = '', headers=dict()) -> \
            Tuple[Response, int]:
        """Wraps response in a consistent format throughout the API.

        Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
        Modifications included:
        - make success a boolean since there's only 2 values
        - make message a single string since we will only use one message per response

        IMPORTANT: data must be a dictionary where:
        - the key is the name of the type of data
        - the value is the data itself

        :param headers <dict> Dictionary of headers
        :param data <dict> optional data
        :param status <int> optional status code, defaults to 200
        :param message <str> optional message
        :returns tuple of Flask Response and int
        """

        if data is not None:
            if not isinstance(data, Dict):
                try:
                    if isinstance(data, Serializable):
                        data = data.to_dict()
                    else:
                        data = data.__dict__
                except AttributeError as err:
                    logger.error('Cannot cast object to dict representation. Raise error.')
                    raise TypeError(f'Data should be a dictionary 😞. {err}')

        # merge default headers with current
        headers = {**self.default_headers, **headers}
        res = {'success': 200 <= status < 300, 'message': message, 'result': data,
               'headers': headers}
        response = jsonify(res)
        response.status_code = status
        return response, status

    def copy(self, response, message=None):
        if response is not None:
            return self.create(data=response.json()['result'], status=response.status_code,
                               message=message if message else response.json()['message'])
        else:
            raise TypeError('Response should not be None')


req = RequestTool()
post = req.post

resp = ResponseTool()
create_response = resp.create
copy_response = resp.copy
