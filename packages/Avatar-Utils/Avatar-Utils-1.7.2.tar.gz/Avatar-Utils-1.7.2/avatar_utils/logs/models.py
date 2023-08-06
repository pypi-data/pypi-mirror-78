import json
from datetime import datetime
from logging import getLogger

from flask import request

from app import db

logger = getLogger(__name__)


def format_text(text):
    return ' '.join(text.strip().split())


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer(), primary_key=True)
    route = db.Column(db.String(100))
    method = db.Column(db.String(10))
    request = db.Column(db.Text())
    response = db.Column(db.Text())
    ts = db.Column(db.DateTime(), default=datetime.utcnow)
    duration = db.Column(db.Integer())
    status_code = db.Column(db.String)
    message = db.Column(db.String)

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
        log = Log()
        log.route = request.path
        log.method = request.method
        log.request = json.dumps(data)
        db.session.add(log)
        db.session.commit()
        return log

    @staticmethod
    def complete(log, response):
        if log:
            log.duration = (datetime.utcnow() - log.ts).total_seconds()
            log.status_code = response.status
            try:
                data = response.json
                log.response = json.dumps(data)
                log.message = data.get('message')
            except TypeError as err:
                log_prefix = f'[ EVENT LOGGING | {request.remote_addr} {request.method} > {request.url_rule} ]'
                logger.warning(f'{log_prefix} < Response is not in JSON format')
                logger.warning(
                    f'{log_prefix} < Message: {err.__class__.__name__}. Errors: {list(str(e) for e in err.args)}')
            db.session.commit()
            return True
        return False

    def delete(self):
        log = Log.query.filter_by(id=self.id).first()
        db.session.delete(log)
        db.session.commit()
