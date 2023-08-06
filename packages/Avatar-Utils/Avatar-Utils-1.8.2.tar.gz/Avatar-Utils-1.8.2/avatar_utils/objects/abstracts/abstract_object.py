from dataclasses import dataclass as python_dataclass, field

from avatar_utils.objects.abstracts.serializable import Serializable


@python_dataclass
class AbstractObject(Serializable):
    pass
