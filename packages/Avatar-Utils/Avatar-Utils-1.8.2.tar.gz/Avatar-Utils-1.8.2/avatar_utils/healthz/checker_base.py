from abc import ABC, abstractmethod
from functools import partial
from logging import getLogger

logger = getLogger(__name__)


class CheckerBase(ABC):

    @abstractmethod
    def __init__(self, name: str, **kwargs):
        self.name: str = name
        self._kwargs: dict = kwargs

    @abstractmethod
    def checker(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    @property
    def call(self) -> partial:
        return partial(self.checker, **self._kwargs)
