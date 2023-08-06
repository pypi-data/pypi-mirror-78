from typing import Optional, Any, List, TypeVar

from app import db


class CRUDMixin:

    @classmethod
    def ensure(cls,
               **kwargs) -> db.Model:
        instance = cls.read(**kwargs)
        return instance if instance is not None else cls.create(**kwargs)

    @classmethod
    def create(cls, **kwargs) -> 'CRUDMixin':
        kwargs = cls._preprocess_params(**kwargs)
        instance = cls(**kwargs)  # noqa
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def all(cls, **kwargs) -> Optional[List['CRUDMixin']]:
        kwargs = cls._preprocess_params(**kwargs)
        return cls.query.filter_by(**kwargs).all()  # noqa

    @classmethod
    def read(cls, **kwargs) -> Optional['CRUDMixin']:
        kwargs = cls._preprocess_params(**kwargs)
        return cls.query.filter_by(**kwargs).first()  # noqa

    def update(self, **kwargs):
        kwargs = self._preprocess_params(**kwargs)
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.flush()

    @classmethod
    def delete(cls, **kwargs):
        kwargs = cls._preprocess_params(**kwargs)
        rec = cls.read(**kwargs)
        db.session.delete(rec)
        db.session.commit()

    @staticmethod
    def _preprocess_params(**kwargs: Any) -> dict:
        return kwargs
