from logging import getLogger
from typing import Optional

from flasgger import Swagger
from flask import Flask
from marshmallow import ValidationError
from requests import post, ConnectionError

from avatar_utils.validation import SuccessResponseSchema
from avatar_utils.validation.constants import ServiceHTTPCodes

logger = getLogger(__name__)


def service_registration(swagger: Swagger,
                         url: str,
                         username: str,
                         password: str,
                         service_name: Optional[str] = None,
                         service_url: Optional[str] = None) -> Optional[dict]:

    app: Flask = swagger.app
    registration_response: Optional[dict] = None

    payload = dict(username=username, password=password, name=service_name, url=service_url)

    with app.app_context():
        spec = swagger.get_apispecs()
        logger.debug(f'spec = {spec}')
        payload.update(dict(api_description=spec))

    payload = dict((k, v) for k, v in payload.items() if v is not None)

    try:
        response = post(url=url, json=payload)

        logger.debug(f'{response.status_code} {response.reason}: {response.text}')
        if response.status_code == ServiceHTTPCodes.OK.value:
            registration_response = SuccessResponseSchema().loads(response.text)
    except ValidationError as err:
        logger.error(f'Incorrect response from server: {err.messages}')
    except TypeError as err:
        logger.error(f'Dump specification to JSON error: {err}')
    except ConnectionError as err:
        logger.error(f'Registration host unavailable: {err}')
    except Exception as err:  # noqa W0703
        logger.error(f'Unknown error ({err.__class__.__name__}) during registration: {err}')

    logger.info(f'Registration state: {"FAIL" if registration_response is None else "PASS"}')
    return registration_response
