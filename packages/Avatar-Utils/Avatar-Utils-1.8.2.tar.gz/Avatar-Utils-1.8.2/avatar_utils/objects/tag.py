from dataclasses import dataclass as python_dataclass

from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts.abstract_object import AbstractObject


@dataclass
@python_dataclass
class Tag(AbstractObject):
    service: str = None
    category: str = None
    text: str = None
    created_at: str = None
    approved_at: str = None
    score: float = None

    repr_type: str = None

    id: int = None
    stars: int = None
