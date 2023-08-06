from logging import getLogger
from typing import Optional, Dict

import requests
from flask import current_app

from avatar_utils.core.lazy_cached_attribute import LazyCachedAttribute

logger = getLogger()


class PlannerAdapter:

    def _make_url(self, rest):
        base_url = current_app.config["PLANNER_URL"]
        return f'{base_url}{rest}'

    _schedule_url = LazyCachedAttribute(method=_make_url, name='_schedule_url', rest='/schedule')
    _unschedule_url = LazyCachedAttribute(method=_make_url, name='_unschedule_url', rest='/unschedule')
    _status_url = LazyCachedAttribute(method=_make_url, name='_status_url', rest='/status')

    def schedule_route_call(self, **kwargs) -> Optional[requests.Response]:
        kwargs['service_name'] = kwargs.get('service_name') or current_app.config["SERVICE_NAME"]
        kwargs['method'] = kwargs.get('method') or 'POST'

        return self._call_http(url=self._schedule_url, json=kwargs)

    def unschedule_route_call(self, **kwargs) -> Optional[requests.Response]:
        kwargs['service_name'] = kwargs.get('service_name') or current_app.config["SERVICE_NAME"]
        kwargs['method'] = kwargs.get('method') or 'POST'

        return self._call_http(url=self._unschedule_url, json=kwargs)

    def status(self, **kwargs) -> Optional[requests.Response]:
        return self._call_http(url=self._unschedule_url, json=kwargs)

    def _call_http(self, url: str, json: dict = None, **kwargs) -> Optional[Dict]:
        response = requests.post(url=url, json=json, **kwargs)

        if response.status_code != 200:
            logger.warning(f'Something went wrong, status code: {response.status_code}. Response: {response.text}')

        return response.json()
