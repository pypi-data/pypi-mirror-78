from logging import getLogger

from flask import g, request
from sqlalchemy.exc import DatabaseError

from . import logs
from .models import *

logger = getLogger(__name__)


@logs.before_app_request
def before_request():
    log_prefix = f'[ LOGGING BEFORE | {request.remote_addr} {request.method} > {request.url_rule} ]'
    try:
        log = Log.init(request)
        g.log = log
    except DatabaseError as err:
        logger.warning(f'{log_prefix} < Rollback transaction due to: {err}')
        db.session.rollback()
    except BaseException as err:
        logger.error(f'{log_prefix} < Error occurs: {err}')


@logs.after_app_request
def after_request(response):
    log_prefix = f'[ LOGGING AFTER | {request.remote_addr} {request.method} > {request.url_rule} ]'
    try:
        if g.log:
            Log.complete(g.log, response)
        else:
            logger.warning('log_id is None, cannot complete logging process')
    except DatabaseError as err:
        logger.warning(f'{log_prefix} < Rollback transaction due to: {err}')
        db.session.rollback()
    except BaseException as err:
        logger.error(f'{log_prefix} < Error occurs: {err}')
    return response
