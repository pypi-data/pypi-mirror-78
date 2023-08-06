import json
from datetime import datetime
from logging import getLogger

from flask import request

from app import db
from ..db.mixins import CRUDMixin

logger = getLogger(__name__)


def format_text(text):
    return ' '.join(text.strip().split())


class Log(CRUDMixin, db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer(), primary_key=True)
    route = db.Column(db.String(100), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    request = db.Column(db.Text(), nullable=False)
    response = db.Column(db.Text(), nullable=True)
    ts = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    duration = db.Column(db.Integer(), nullable=True)
    status_code = db.Column(db.String, nullable=True)
    message = db.Column(db.String, nullable=True)

    def __repr__(self):
        return """<log object>
        id: {}
        route: {}
        method: {}
        request: {}
        response: {}
        ts: {}
        duration: {}
        status_code: {}
        message: {}""".format(self.id, self.route, self.method, self.request, self.response, self.ts,
                              self.duration, self.status_code, self.message)

    @staticmethod
    def init(request):
        data = request.json
        log = Log.create(route=request.path, method=request.method, request=json.dumps(data))
        return log

    @staticmethod
    def complete(log, response):
        if log:
            log.update(duration=(datetime.utcnow() - log.ts).total_seconds(), status_code=response.status)
            try:
                data = response.json
                log.update(response=json.dumps(data), message=data.get('message'))
            except TypeError as err:
                log_prefix = f'[ EVENT LOGGING | {request.remote_addr} {request.method} > {request.url_rule} ]'
                logger.warning(f'{log_prefix} < Response is not in JSON format')
                logger.warning(
                    f'{log_prefix} < Message: {err.__class__.__name__}. Errors: {list(str(e) for e in err.args)}')
            db.session.commit()
            return True
        return False
