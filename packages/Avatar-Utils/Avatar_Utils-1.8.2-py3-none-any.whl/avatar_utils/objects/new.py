from dataclasses import dataclass as python_dataclass
from typing import Any, List

from marshmallow_dataclass import dataclass

from avatar_utils.objects import Image
from avatar_utils.objects.abstracts.abstract_object import AbstractObject


@dataclass
@python_dataclass
class New(AbstractObject):
    title: str = None
    text: str = None
    preview_text: str = None

    date_appeared: str = None

    origin: str = None
    url: str = None
    location: str = None
    author: str = None
    image: Image = None
    tags: List[Any] = None

    repr_type: str = None

    id: int = None
    stars: int = None
