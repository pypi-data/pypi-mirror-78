from dataclasses import dataclass as python_dataclass, field

from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts.abstract_object import AbstractObject


@dataclass
@python_dataclass
class Message(AbstractObject):
    text: str = None

    repr_type: str = None

    id: int = None
    stars: int = None
