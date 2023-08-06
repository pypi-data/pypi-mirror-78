from typing import Optional, Tuple, Dict

from flask import request
from requests import Session

from avatar_utils.sso_helper.constants import (
    AUTH_HEADER_NAME,
    DEFAULT_TOKEN_TYPE,
)


class FlaskAuthHeader:

    @staticmethod
    def from_request() -> Optional[str]:

        return request.headers.get(AUTH_HEADER_NAME)

    @classmethod
    def request_token(cls) -> Optional[str]:

        value, _ = cls.extract()
        return value

    @classmethod
    def request_token_type(cls) -> Optional[str]:

        _, value = cls.extract()
        return value

    @classmethod
    def extract(cls) -> Tuple[Optional[str], Optional[str]]:

        raw_value = cls.from_request()
        token_data = raw_value.split(' ') if raw_value else (None, None)
        token_type, token_string = token_data
        return token_string, token_type

    @classmethod
    def make_header_value(cls,
                          token_string: Optional[str] = None,
                          token_type: Optional[str] = None) -> Optional[str]:

        if not token_type and token_string and token_string.startswith(DEFAULT_TOKEN_TYPE):
            token_type, token_string = token_string.split(' ')

        if not token_type and token_string:
            token_type = DEFAULT_TOKEN_TYPE

        if not token_type and not token_string:
            token_string, token_type = cls.extract()

        return f'{token_type} {token_string}'

    @classmethod
    def make_header_dict(cls,
                         token_string: Optional[str] = None,
                         token_type: Optional[str] = None) -> Dict[str, Optional[str]]:

        value = cls.make_header_value(token_string, token_type)
        return {AUTH_HEADER_NAME: value}

    @classmethod
    def make_session(cls,
                     token_string: Optional[str] = None,
                     token_type: Optional[str] = None) -> Optional[Session]:
        session = Session()
        header = cls.make_header_dict(token_string=token_string, token_type=token_type)
        if header[AUTH_HEADER_NAME] is not None:
            session.headers.update(header)
            return session
