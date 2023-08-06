from dataclasses import dataclass as python_dataclass

from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts.abstract_object import AbstractObject
from avatar_utils.objects.person import Person


@dataclass
@python_dataclass
class Match(AbstractObject):
    person1: Person = None
    person2: Person = None

    repr_type: str = None

    score: float = None

    id: int = None
    stars: int = None
