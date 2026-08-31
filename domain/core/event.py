from datetime import datetime
from uuid import UUID

from domain.core.errors import ReadOnlyField


class Event:
    def __init__(
        self,
        id: UUID = None,
        date: datetime = None,
        created_at: datetime = None,
        **kwargs
    ):
        self._id = id
        self._date = date
        self._created_at = created_at

        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def type(self) -> str:
        return self.__class__.__name__

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @id.setter
    def id(self, value: UUID):
        if self._id is not None:
            raise ReadOnlyField('id')

        self._id = value

    @date.setter
    def date(self, value: datetime):
        if self._date is not None:
            raise ReadOnlyField('date')

        self._date = value

    @created_at.setter
    def created_at(self, value: datetime):
        if self._created_at is not None:
            raise ReadOnlyField('created_at')

        self._created_at = value

    def get_metadata(self) -> dict:
        raise NotImplementedError()
