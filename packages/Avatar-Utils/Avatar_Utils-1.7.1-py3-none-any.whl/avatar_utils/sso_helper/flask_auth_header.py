from typing import Optional, Tuple, Dict

from flask import request

from avatar_utils.sso_helper.constants import (
    AUTH_HEADER_NAME,
    DEFAULT_TOKEN_TYPE,
)


class FlaskAuthHeader:

    @property
    def from_request(self) -> Optional[str]:

        return request.headers.get(AUTH_HEADER_NAME)

    @property
    def request_token(self) -> Optional[str]:

        value, _ = self.extract()
        return value

    @property
    def request_token_type(self) -> Optional[str]:

        _, value = self.extract()
        return value

    def extract(self) -> Tuple[Optional[str], Optional[str]]:

        raw_value = self.from_request
        token_data = raw_value.split(' ') if raw_value else (None, None)
        token_type, token_string = token_data
        return token_string, token_type

    def make_header_value(self,
                          token_string: Optional[str] = None,
                          token_type: Optional[str] = None) -> Optional[str]:

        if not token_type and token_string and token_string.startswith(DEFAULT_TOKEN_TYPE):
            token_type, token_string = token_string.split(' ')

        if not token_type and token_string:
            token_type = DEFAULT_TOKEN_TYPE

        if not token_type and not token_string:
            token_string, token_type = self.extract()

        return f'{token_type} {token_string}'

    def make_header_dict(self,
                         token_string: Optional[str] = None,
                         token_type: Optional[str] = None) -> Dict[str, Optional[str]]:

        value = self.make_header_value(token_string, token_type)
        return {AUTH_HEADER_NAME: value}
