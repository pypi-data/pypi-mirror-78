import traceback
from functools import wraps
from logging import getLogger
from typing import Type, Optional, Union, Callable, Tuple, Sequence

from flask import request, jsonify
from marshmallow import Schema
from marshmallow import ValidationError
from sqlalchemy.exc import DatabaseError
from werkzeug import Response, exceptions  # noqa: PyPackageRequirements

from avatar_utils.core import create_response
from avatar_utils.validation.constants import ServiceHTTPCodes

logger = getLogger(__name__)

DEFAULT_VALIDATE_METHOD = 'GET'


def validate_json(request_schema: Optional[Type[Schema]] = None,
                  response_schema: Optional[Type[Schema]] = None,
                  methods: Union[str, Sequence[str]] = DEFAULT_VALIDATE_METHOD) -> Callable:
    if isinstance(methods, str):
        methods = {methods}

    methods = set(m.upper().strip() for m in methods)

    def decorator(f) -> Callable:

        @wraps(f)
        def wrapper(*args, **kw) -> Union[str, Tuple[Response, int]]:

            log_prefix = f'[ VALIDATION | {request.remote_addr} {request.method} > {request.url_rule} ]'
            step = 'pre processing'

            try:
                # skip decorator if unexpected HTTP method of request
                if request.method not in methods:
                    logger.debug(f'{log_prefix} skip {request.method} method, validator expect {methods}')
                    return f(*args, **kw)

                # validate request data
                step = 'validate request data'
                if request_schema:
                    validation_schema = request_schema()

                    if not request.is_json:
                        logger.warning(f'{log_prefix} < invalid content-type header')
                        return create_response(status=ServiceHTTPCodes.BAD_REQUEST.value,
                                               message='invalid content-type header')

                    validation_schema.load(request.json)
                    logger.debug(f'{log_prefix} request body validated')

                # call HTTP handler
                step = 'call HTTP handler'
                status = 200
                result = f(*args, **kw)
                if isinstance(result, tuple):
                    response, status = result
                else:
                    response = result

                if not isinstance(response, Response):
                    response = jsonify(result)

                # validate response data
                step = 'validate response data'
                if response_schema:
                    validation_schema = response_schema()

                    if response.status_code != ServiceHTTPCodes.OK.value:
                        return response, status

                    data = validation_schema.load(response.json)
                    logger.debug(f'{log_prefix} response validated')
                    response = jsonify(validation_schema.dump(data))

            except exceptions.BadRequest as err:
                logger.warning(f'{log_prefix} < Step: {step}. Exception: {err}')
                response, status = create_response(status=ServiceHTTPCodes.BAD_REQUEST.value,
                                                   message='invalid requests body')
            except ValidationError as err:
                logger.warning(f'{log_prefix} < Step: {step}. Exception: {err}')
                response, status = create_response(status=ServiceHTTPCodes.UNPROCESSABLE_ENTITY.value,
                                                   message='validation error',
                                                   data=dict(err.messages))
            except NotImplementedError as err:
                logger.warning(f'{log_prefix} < Step: {step}. Exception: {err}')
                response, status = create_response(status=ServiceHTTPCodes.NOT_IMPLEMENTED.value,
                                                   message=type(err).__name__,
                                                   data=dict(traceback=str(traceback.format_exc())))
            except DatabaseError as err:
                logger.warning(f'{log_prefix} < Step: {step}. Exception: {err}')
                try:
                    from app import db
                    logger.debug('db imported from app')
                    db.session.rollback()
                except ImportError:
                    logger.info('Cannot import db from app. Skip.')
                response, status = create_response(status=ServiceHTTPCodes.SERVER_ERROR.value,
                                                   message=type(err).__name__,
                                                   data=dict(traceback=str(traceback.format_exc())))
            except (TypeError, Exception) as err:  # noqa
                logger.warning(f'{log_prefix} < Step: {step}. Exception: {err}')
                response, status = create_response(status=ServiceHTTPCodes.SERVER_ERROR.value,
                                                   message=type(err).__name__,
                                                   data=dict(traceback=str(traceback.format_exc())))

            return response, status

        return wrapper

    return decorator
