from typing import Optional
import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.product.models import Product
from settings.repositories import SQLAlchemyORMRepository
from utils import with_session


class ProductRepository(SQLAlchemyORMRepository[Product]):
    cls_model = Product

    @with_session
    async def find_all_available_products(
        self,
        *,
        session: Optional[AsyncSession] = None,
    ) -> list[Product]:
        assert isinstance(session, AsyncSession), "В repository не передана сессия"

        stmt = select(Product).where(Product.available_stock > 0)
        result = await session.execute(stmt)

        return list(result.scalars().all())

    @with_session
    async def reduce_product_amount(
        self,
        id: uuid.UUID,
        amount: int,
        *,
        session: Optional[AsyncSession] = None,
    ) -> Product:
        assert isinstance(session, AsyncSession), "В repository не передана сессия"

        product: Product = await self.find_one(id=id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Товар не найден.",
            )
        if amount > product.available_stock:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Недостаточно товара.",
            )

        return await self.update_one(
            data={"available_stock": product.available_stock - amount},
            id=id,
        )
