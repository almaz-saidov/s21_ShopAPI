import uuid
from typing import Optional, Union

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from apps.address.models import Address
from apps.address.repositories import AddressRepository
from apps.client.models import Client
from settings.repositories import SQLAlchemyORMRepository
from utils import with_session


class ClientRepository(SQLAlchemyORMRepository[Client]):
    cls_model = Client

    @with_session
    async def find_clients(
        self,
        offset: Union[int, None],
        limit: Union[int, None],
        *,
        session: Optional[AsyncSession] = None,
    ) -> list[Client]:
        assert isinstance(session, AsyncSession), "В repository не передана сессия"

        stmt = (
            select(self.model)
            .options(joinedload(Client.address))
        )

        if offset is not None and limit is not None:
            stmt = stmt.offset(offset).limit(limit)

        result = await session.execute(stmt)
        return list(result.scalars().all())

    @with_session
    async def find_client(
        self,
        *,
        session: Optional[AsyncSession] = None,
        **filter_by,
    ) -> Optional[Client]:
        assert isinstance(session, AsyncSession), "В repository не передана сессия"

        stmt = (
            select(self.model)
            .options(joinedload(Client.address))
            .filter_by(**filter_by)
            .limit(1)
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @with_session
    async def update_client_address(
        self,
        id: uuid.UUID,
        data: dict,
        *,
        session: Optional[AsyncSession] = None,
    ) -> Client:
        assert isinstance(session, AsyncSession), "В repository не передана сессия"

        client = await self.find_one(
            id=id,
            session=session,
        )
        if client is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Клиент не найден.",
            )

        if client.address_id is None:
            added_address: Address = await AddressRepository().add_one(
                data=data,
                session=session,
            )
        else:
            added_address: Address = await AddressRepository().update_one(
                data=data,
                id=client.address_id,
                session=session,
            )

        stmt = update(Client).filter_by(id=id).values(address_id=added_address.id)
        await session.execute(stmt)
        await session.commit()

        return await self.find_client(id=id)
