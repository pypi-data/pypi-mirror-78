from dataclasses import dataclass as python_dataclass, field
from typing import List, Any

from marshmallow_dataclass import dataclass

from avatar_utils.objects.abstracts.serializable import Serializable


@dataclass
@python_dataclass
class FeedItem(Serializable):
    objects: List[Any] = field(default_factory=list)

    id: int = None

    service: str = None
    service_header: str = None
    route: str = None

    pinned: bool = None
    score: float = None
    date: str = None

    pop_up: bool = None
    url: str = None

    label: str = None

    repr_type: str = None
