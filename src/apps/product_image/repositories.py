import uuid
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.product.repositories import ProductRepository
from apps.product_image.models import ProductImage
from settings.repositories import SQLAlchemyORMRepository
from utils import with_session


class ProductImageRepository(SQLAlchemyORMRepository[ProductImage]):
    cls_model = ProductImage

    @with_session
    async def add_image(
        self,
        id: uuid.UUID,
        data: dict,
        *,
        session: Optional[AsyncSession] = None,
    ) -> ProductImage:
        assert isinstance(session, AsyncSession), "В repository не передана сессия"

        product = await ProductRepository().find_one(id=id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Товар не найден.",
            )

        added_image = await self.add_one(data=data)

        await ProductRepository().update_one(
            data={"image_id": added_image.id},
            id=id,
        )

        return added_image
