from logging import getLogger

import requests
from flask import current_app

logger = getLogger()


class PlannerAdapter:

    @property
    def _planner_schedule_url(self):
        return f'{current_app.config["PLANNER_URL"]}/schedule'

    @property
    def _planner_unschedule_url(self):
        return f'{current_app.config["PLANNER_URL"]}/unschedule'

    def schedule_route_call(self, **kwargs):
        kwargs = {
            'service_name': kwargs.get('service_name') or current_app.config["SERVICE_NAME"],
            'route': kwargs['route'],
            'route_args': kwargs.get('route_args') or {},
            'method': kwargs.get('method') or 'POST',
            'trigger_type': kwargs['trigger_type'],
            'trigger_args': kwargs['trigger_args']
        }

        requests.post(self._planner_schedule_url, json=kwargs)

    def unschedule_route_call(self, **kwargs):
        kwargs = {
            'service_name': kwargs.get('service_name') or current_app.config["SERVICE_NAME"],
            'route': kwargs['route'],
            'method': kwargs.get('method') or 'POST'
        }

        requests.post(self._planner_unschedule_url, json=kwargs)
