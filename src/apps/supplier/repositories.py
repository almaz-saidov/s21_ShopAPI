import uuid
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from apps.address.models import Address
from apps.address.repositories import AddressRepository
from apps.supplier.models import Supplier
from settings.repositories import SQLAlchemyORMRepository
from utils import with_session


class SupplierRepository(SQLAlchemyORMRepository[Supplier]):
    cls_model = Supplier

    @with_session
    async def find_suppliers(
        self,
        *,
        session: Optional[AsyncSession] = None,
    ) -> list[Supplier]:
        assert isinstance(session, AsyncSession), "В repository не передана сессия"

        stmt = (
            select(Supplier)
            .options(joinedload(Supplier.address))
        )

        result = await session.execute(stmt)
        return list(result.scalars().all())

    @with_session
    async def find_supplier(
        self,
        *,
        session: Optional[AsyncSession] = None,
        **filter_by,
    ) -> Optional[Supplier]:
        assert isinstance(session, AsyncSession), "В repository не передана сессия"

        stmt = (
            select(self.model)
            .options(joinedload(Supplier.address))
            .filter_by(**filter_by)
            .limit(1)
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @with_session
    async def update_supplier_address(
        self,
        id: uuid.UUID,
        data: dict,
        *,
        session: Optional[AsyncSession] = None,
    ) -> Supplier:
        assert isinstance(session, AsyncSession), "В repository не передана сессия"

        supplier = await self.find_one(
            id=id,
            session=session,
        )
        if supplier is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Клиент не найден.",
            )

        if supplier.address_id is None:
            added_address: Address = await AddressRepository().add_one(
                data=data,
                session=session,
            )
        else:
            added_address: Address = await AddressRepository().update_one(
                data=data,
                id=supplier.address_id,
                session=session,
            )

        stmt = update(Supplier).filter_by(id=id).values(address_id=added_address.id)
        await session.execute(stmt)
        await session.commit()

        return await self.find_supplier(id=id)
