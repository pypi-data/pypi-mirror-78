from dataclasses import dataclass as python_dataclass, field
from typing import List

from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts.abstract_object import AbstractObject


@dataclass
@python_dataclass
class Article(AbstractObject):
    author_list: List[str] = field(default_factory=list)
    title: str = None
    journal_info: str = None
    source: str = None

    repr_type: str = None

    id: int = None
    stars: int = None

