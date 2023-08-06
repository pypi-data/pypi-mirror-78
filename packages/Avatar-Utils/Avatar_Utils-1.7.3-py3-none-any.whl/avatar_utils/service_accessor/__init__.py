from logging import getLogger
from typing import Dict, Optional

from flask import current_app

from avatar_utils.sso_helper import FlaskAuthHeader

logger = getLogger()


class ServiceAccessor:
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
    def tags_url(self):
        return f'{current_app.config["BACKEND_URL"]}/tags/categories'

    def call_http_with_user_creds(self, url: str, json: dict = None) -> Optional[Dict]:
        try:
            session = FlaskAuthHeader.make_session()
            response = session.post(url=url, json=json)
        except Exception as err:
            logger.warning(f'Error occurs while http call: %s', err)
            return

        if response.status_code == 200 and response.json()['success']:
            return response.json()

        logger.warning(f'Something went wrong status code: {response.status_code}. Response: {response.text}')


service_accessor = ServiceAccessor()
