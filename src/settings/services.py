from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from settings.repositories import AbstractRepository, SQLAlchemyORMRepository

T = TypeVar("T", bound=SQLAlchemyORMRepository)


class AbstractService(ABC):
    @abstractmethod
    def __init__(self, repo: Type[AbstractRepository]) -> None: ...


class BaseService(AbstractService, Generic[T]):
    def __init__(self, repo: Type[T]) -> None:
        self.repository: T = repo()
