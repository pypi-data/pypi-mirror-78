from dataclasses import dataclass as python_dataclass

from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts.abstract_object import AbstractObject


@dataclass
@python_dataclass
class Image(AbstractObject):
    url: str = None
    caption: str = None

    repr_type: str = None

    id: int = None
    stars: int = None
