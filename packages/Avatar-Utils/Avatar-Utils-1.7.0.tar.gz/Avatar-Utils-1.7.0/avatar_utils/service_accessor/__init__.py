from logging import getLogger
from typing import Dict

import requests
from flask import current_app

logger = getLogger()


class ServiceAccessor:
    auth_header = None

    @property
    def user_match_url(self):
        return f'{current_app.config["BACKEND_URL"]}/da/user/match'

    @property
    def services_url(self):
        return f'{current_app.config["BACKEND_URL"]}/proxy/services'

    @property
    def service_list_url(self):
        return f'{current_app.config["BACKEND_URL"]}/proxy/service_list'

    @property
    def __login_url(self):
        return f'{current_app.config["BACKEND_URL"]}/login'

    def __refresh_token(self):
        response = requests.post(self.__login_url, json=dict(username=current_app.config['BACKEND_USERNAME'],
                                                             password=current_app.config['BACKEND_PASSWORD']))
        auth_header = None
        if response.status_code == 200:
            token = response.json()['result']['token']
            auth_header = {'Authorization': f'Bearer {token}'}
        elif response.status_code == 500:
            logger.error(f'Received status 500. Response: {response.text}')
        else:
            logger.error(
                f'Cannot login {self.__login_url}. Status: {response.status_code}. Response: {response.text}')
            raise ConnectionError

        self.auth_header = auth_header

    def call_http(self, url: str, headers: dict = {}, data: dict = {}) -> Dict:
        # first call
        if not self.auth_header:
            self.__refresh_token()

        headers = {**self.auth_header, **headers}

        response = requests.post(url, headers=headers, json=data)

        if response.status_code in [401, 403]:
            self.__refresh_token()
            return self.call_http(url=url, headers=headers, data=data)
        elif response.status_code == 200:
            if response.json()['success']:
                return response.json()

        logger.warning(f'Something went wrong status code: {response.status_code}. Response: {response.text}')
        return {}


service_accessor = ServiceAccessor()
