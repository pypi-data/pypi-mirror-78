import logging
from json import dumps as json_dumps

import flask

JSON_DECODE_ATTRS = dict(indent=2, ensure_ascii=False)

logger = logging.getLogger(__name__)


class AbstractApp:
    client = None
    headers = {'Content-type': 'application/json'}

    def post(self, url, data=dict()) -> flask.Response:
        return self.client.post(url, json=data, headers=self.headers)

    def get(self, url, data=dict()) -> flask.Response:
        return self.client.get(url, json=data, headers=self.headers)

    def register(self, username, email, password, confirm) -> flask.Response:
        return self.post('/register', data=dict(username=username, email=email, password=password, confirm=confirm))

    def login(self, username, password) -> flask.Response:
        return self.post('/login', data=dict(username=username, password=password))

    def logout(self) -> flask.Response:
        return self.post('/logout')

    def delete(self, user_id, password):
        return self.post('/user/delete', data=dict(user_id=user_id, password=password))

    def rprint(self, response):
        if not isinstance(response, flask.Response):
            logger.warning(f'rprint prints only flask.Response class data')
            return

        json = response.json
        if json:
            logger.debug(json)
        else:
            logger.debug(response.data.decode())

    def json_dumps(self, data):
        return json_dumps(data, **JSON_DECODE_ATTRS)
