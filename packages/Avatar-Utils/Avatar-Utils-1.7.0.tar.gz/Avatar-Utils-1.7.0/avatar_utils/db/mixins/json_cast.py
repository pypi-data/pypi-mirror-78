from json import loads, dumps
from typing import Union, Any

from app import db


class JsonCastMixin:

    def __init__(self):
        try:
            self.db = db
        except:  # noqa
            self.db = None

    def str_field_json_loads(
            self,
            field_name: str,
            **kwargs,
    ) -> Union[str, list, dict]:

        value: str = getattr(self, field_name)
        if not isinstance(value, str):
            raise KeyError

        return loads(value, **kwargs)

    def filter_by_json_str_field(
            self,
            field_name: str,
            value: Union[str, list, tuple, dict],
            **kwargs: Any,
    ) -> object:

        stored_value: str = getattr(self, field_name)
        if not isinstance(stored_value, str):
            raise KeyError
        kwargs.update({field_name: dumps(value)})

        return db.query.filter_by(**kwargs)
