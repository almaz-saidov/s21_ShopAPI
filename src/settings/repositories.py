from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, Type, TypeVar

from sqlalchemy import asc, delete, desc, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from settings.database import Base
from utils import with_session

T = TypeVar("T", bound=Base)


class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    async def add_one(self, data: dict, *args, **kwargs) -> T: ...

    @abstractmethod
    async def find_one(
        self, order_by: Optional[list[tuple[str, str]]], *args, **filter_by
    ) -> Optional[T]: ...

    @abstractmethod
    async def find_all(self, *args, **filter_by) -> list[T]: ...

    @abstractmethod
    async def update_one(self, data: dict, *args, **filter_by) -> Optional[T]: ...

    @abstractmethod
    async def force_delete_one(self, *args, **filter_by) -> None: ...


class SQLAlchemyORMRepository(AbstractRepository[T]):
    cls_model: Optional[Type[T]] = None

    def __init__(
        self,
        model: Optional[Type[T]] = None,
    ):
        orm_model: Optional[Type[T]] = model or self.__class__.cls_model
        if not orm_model:
            raise ValueError("Необходимо передать модель в класс или при инициализации репозитория.")
        self.model: Type[T] = orm_model

    @with_session
    async def add_one(
        self,
        data: dict[str, Any],
        *,
        session: Optional[AsyncSession] = None,
    ) -> T:
        assert isinstance(session, AsyncSession), "В repository не передана сессия"

        stmt = insert(self.model).values(**data).returning(self.model)
        result = await session.execute(stmt)
        await session.commit()
        return result.scalar_one()

    @with_session
    async def find_one(
        self,
        *,
        session: Optional[AsyncSession] = None,
        **filter_by,
    ) -> Optional[T]:
        assert isinstance(session, AsyncSession), "В repository не передана сессия"

        stmt = select(self.model).filter_by(**filter_by).limit(1)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @with_session
    async def find_all(
        self,
        *,
        order_by: Optional[list[tuple[str, str]]] = None,
        session: Optional[AsyncSession] = None,
        **filter_by,
    ) -> list[T]:
        assert isinstance(session, AsyncSession), "В repository не передана сессия"

        stmt = select(self.model).filter_by(**filter_by)

        if not order_by:
            order_by = []

        order_by_clauses = []
        for field_name, direction in order_by:
            if not hasattr(self.model, field_name):
                raise ValueError(
                    f"Поле '{field_name}' не существует у модели '{self.model.__name__}'"
                )
            column = getattr(self.model, field_name)
            if direction.lower() == "asc":
                order_by_clauses.append(asc(column))
            elif direction.lower() == "desc":
                order_by_clauses.append(desc(column))
            else:
                raise ValueError(f"Некорректный способ сортировки '{direction}' для поля '{field_name}'. Используйте 'asc' или 'desc'.")

        stmt = stmt.order_by(*order_by_clauses)

        result = await session.execute(stmt)
        return list(result.scalars().all())

    @with_session
    async def update_one(
        self,
        data: dict,
        *,
        session: Optional[AsyncSession] = None,
        **filter_by,
    ) -> Optional[T]:
        assert isinstance(session, AsyncSession), "В repository не передана сессия"

        stmt = update(self.model).filter_by(**filter_by).values(**data).returning(self.model)
        result = await session.execute(stmt)
        obj = result.scalar_one_or_none()
        await session.commit()
        return obj

    @with_session
    async def force_delete_one(
        self,
        *,
        session: Optional[AsyncSession] = None,
        **filter_by,
    ) -> None:
        assert isinstance(session, AsyncSession), "В repository не передана сессия"

        stmt = delete(self.model).filter_by(**filter_by)
        await session.execute(stmt)
        await session.commit()
