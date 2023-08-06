from dataclasses import dataclass as python_dataclass, field
from typing import List, Any

from marshmallow_dataclass import dataclass

from avatar_utils.objects import Image
from avatar_utils.objects.abstracts.abstract_object import AbstractObject


@dataclass
@python_dataclass
class Person(AbstractObject):
    tags: List[Any] = field(default_factory=list)
    lastname: str = None
    firstname: str = None
    middlename: str = None
    image: Image = None
    url: str = None
    contacts: str = None

    repr_type: str = None

    id: int = None
    stars: int = None
