from datetime import timedelta
from functools import partial
from time import time
from typing import Optional, Dict, Any, List, Union

from flasgger import swag_from
from flask import Flask, Blueprint

from avatar_utils.healthz.checker_base import CheckerBase
from avatar_utils.healthz.utils import make_app_info
from avatar_utils.validation.schemas import RootResponseSchema

blueprint = Blueprint('healthz', __name__)

FLASGGER_INFO_DECORATOR = swag_from(dict(description='General information about service',
                                         tags=[blueprint.name],
                                         responses={200: {'description': 'Success response',
                                                          'schema': RootResponseSchema}}))
FLASGGER_PING_DECORATOR = swag_from(dict(description='Ping route',
                                         tags=[blueprint.name]))
FLASGGER_HEALTHZ_DECORATOR = swag_from(dict(description='Health checking',
                                            tags=[blueprint.name]))


def make_info_route(app_name: str,
                    app_version: Optional[str]) -> Dict[str, Any]:
    return make_app_info(app_name=app_name, app_version=app_version)


def make_healthz_route(health_checkers: List[CheckerBase]):

    response = dict()
    response.update({
        'health_checkers': list(),
        'healthy': True
    })

    for health_checker in health_checkers:
        started_at = time()
        passed = health_checker.call()
        finished_at = time() - started_at
        elapsed_time = timedelta(seconds=finished_at)

        if not passed:
            response['all_done'] = False

        response['health_checkers'].append({
            'name': health_checker.name,
            'passed': passed,
            'elapsed': str(elapsed_time),
        })

    return response


def make_healthz_blueprint(app_name: str,
                           app_version: Optional[str] = None,
                           flask_app: Optional[Flask] = None,
                           url_prefix: Optional[str] = None,
                           health_checkers: Optional[Union[CheckerBase,
                                                           List[CheckerBase]]] = None) -> Blueprint:

    if not health_checkers:
        health_checkers = list()

    if isinstance(health_checkers, CheckerBase):
        health_checkers = [health_checkers]

    info_route = partial(make_info_route, app_name=app_name, app_version=app_version)
    healthz_route = partial(make_healthz_route, health_checkers=health_checkers)

    blueprint.add_url_rule('/', 'info_route', FLASGGER_INFO_DECORATOR(info_route))
    blueprint.add_url_rule('/ping', 'ping_route', FLASGGER_PING_DECORATOR(lambda: 'pong'))
    blueprint.add_url_rule('/healthz', 'healthz_route', FLASGGER_HEALTHZ_DECORATOR(healthz_route))

    if flask_app is not None:
        flask_app.register_blueprint(blueprint,
                                     url_prefix=url_prefix)

    return blueprint
