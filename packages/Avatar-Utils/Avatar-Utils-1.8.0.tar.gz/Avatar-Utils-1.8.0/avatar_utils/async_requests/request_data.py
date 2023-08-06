from dataclasses import dataclass, field
from json import dumps
from sys import getsizeof
from typing import Optional

from aiohttp import ClientTimeout
from marshmallow import Schema, fields


class RequestDataSchema(Schema):
    service_name = fields.Str(required=True)
    url = fields.Str(required=True)
    method = fields.Str(required=False, default='GET')
    count = fields.Int(required=False, default=1)
    timeout = fields.Int(required=False, allow_none=True, default=None)
    headers = fields.Dict(required=False, allow_none=True, default=None)
    json = fields.Dict(required=False, allow_none=True, default=None)


@dataclass
class RequestData:
    service_name: str
    url: str
    method: str = 'GET'
    count: int = 1
    timeout: Optional[ClientTimeout] = None
    headers: Optional[dict] = None
    json: Optional[dict] = None

    size: int = field(init=False)

    def __post_init__(self):
        self.size = 0
        if self.json is not None:
            self.size = getsizeof(dumps(self.json))

    @staticmethod
    def make(request_data):
        req_schema = RequestDataSchema()

        if isinstance(request_data, str):
            request_data = dict(url=request_data)

        if isinstance(request_data, dict):
            req_schema.load(request_data)
            request_data = req_schema.dump(request_data)

        if not isinstance(request_data, RequestData):
            seconds = request_data.get('timeout')
            timeout = ClientTimeout(total=0 if seconds is None else seconds)
            return RequestData(service_name=request_data['service_name'],
                               method=request_data['method'],
                               url=request_data['url'],
                               headers=request_data['headers'],
                               count=request_data['count'],
                               json=request_data['json'],
                               timeout=timeout)
        return request_data
