from logging import getLogger
from typing import Dict, Optional

from flask import current_app
from requests import Session

from avatar_utils.core.lazy_cached_attribute import LazyCachedAttribute
from avatar_utils.sso_helper import FlaskAuthHeader

logger = getLogger()


class ServiceAccessor:

    def _make_url(self, rest):
        backend_url = current_app.config["BACKEND_URL"]
        return f'{backend_url}{rest}'

    _user_match_url = LazyCachedAttribute(method=_make_url, name='_user_match_url', rest='/da/user/match')
    _services_url = LazyCachedAttribute(method=_make_url, name='_user_match_url', rest='/proxy/services')
    _service_list_url = LazyCachedAttribute(method=_make_url, name='_user_match_url', rest='/proxy/service_list')
    _tags_url = LazyCachedAttribute(method=_make_url, name='_user_match_url', rest='/tags/categories')
    _user_logs_url = LazyCachedAttribute(method=_make_url, name='_user_match_url', rest='/logs/user')

    def user_match(self, json: Dict = None, **kwargs):
        return self.call_arbitrary_http(url=self._user_match_url, json=json, **kwargs)

    def services(self, json: Dict = None, **kwargs):
        return self.call_arbitrary_http(url=self._services_url, json=json, **kwargs)

    def service_list(self, json: Dict = None, **kwargs):
        return self.call_arbitrary_http(url=self._service_list_url, json=json, **kwargs)

    def tags(self, json: Dict = None, **kwargs):
        return self.call_arbitrary_http(url=self._tags_url, json=json, **kwargs)

    def user_logs(self, json: Dict = None, **kwargs):
        return self.call_arbitrary_http(url=self._user_logs_url, json=json, **kwargs)

    def call_arbitrary_http(self, url: str, json: dict = None, **kwargs) -> Optional[Dict]:
        session: Session = FlaskAuthHeader.make_session()
        response = session.post(url=url, json=json, **kwargs)

        if response.status_code != 200:
            logger.warning(f'Something went wrong, status code: {response.status_code}. Response: {response.text}')

        return response.json()


service_accessor = ServiceAccessor()
